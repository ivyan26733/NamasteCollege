from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login


from post.models import Post, Follow, Stream
from django.contrib.auth.models import User
from authy.models import Profile
from .forms import EditProfileForm, UserRegisterForm
from django.urls import resolve
from comment.models import Comment

@login_required
def UserProfile(request, username):
    Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favourite.all()
    
    # Profile Stats
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    # count_comment = Comment.objects.filter(post=posts).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    # pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'profile':profile,
        'posts_count':posts_count,
        'following_count':following_count,
        'followers_count':followers_count,
        'posts_paginator':posts_paginator,
        'follow_status':follow_status,
        # 'count_comment':count_comment,
    }
    return render(request, 'profile.html', context)

def EditProfile(request):
    user = request.user.id
    print(user)
    profile = Profile.objects.get(user__id=user)
    print(profile)

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        print("HELO1")
        if form.is_valid():
            print("HELO2")
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            # profile.location = form.cleaned_data.get('location')
            # profile.url = form.cleaned_data.get('url')
            # profile.bio = form.cleaned_data.get('bio')
            profile.faculty = form.cleaned_data.get('faculty')
            profile.course = form.cleaned_data.get('course')
            profile.branch = form.cleaned_data.get('branch')
            profile.year = form.cleaned_data.get('year')
            profile.save()
            return redirect('profile', profile.user.username)
        else:
         print(form.errors)

    else:
        form = EditProfileForm(instance=request.user.profile)

    context = {
        'form':form,
    }
    return render(request, 'editprofile.html', context)

def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try:
        f, created = Follow.objects.get_or_create(follower=request.user, following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:25]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=request.user, date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))
    


from .models import Roll
from django.core.mail import send_mail
from ig_prj.settings import EMAIL_HOST_USER
import random


def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        # print(password1)
        password2 = request.POST.get('password2')

        form = UserRegisterForm(request.POST)
        # username = form.cleaned_data['username']

        # username = form.cleaned_data.get('username')

        if form.is_valid():
            # username = form.cleaned_data.get('username')

            # Check if username already exists in the Roll model
            if Roll.objects.filter(roll=username).exists():
            #  new_user = form.save()
             otp = random.randint(100000, 999999)
             send_mail("User Data: ", f"Verify Your Email by the OTP:  {otp}", EMAIL_HOST_USER, [email], fail_silently=True)
             request.session['password'] = password1

            # Profile.get_or_create(user=request.user)
            # username = form.cleaned_data.get('username')
             messages.success(request, f'Congratulations you have been successfully Registered!!')
             return render(request, 'verify.html', {'otp':otp, 'username':username, 'email':email, 'password1':password1, 'password2':password2})
            
            # elif User.objects.filter(username=username).first():
            #     print("sdbhbchebchbhvbhdebfvhebfvfecbhbdvbdjvvvvvvvvvjbfeidbd")
            #     messages.error(request, 'Username already exists in the Roll model. Please choose a different username.')
            
            else:
              messages.error(request, 'Your Roll Number is not in University Data. You can not register')
              
        

            # Automatically Log In The User
            # new_user = authenticate(username=form.cleaned_data['username'],
                                    # password=form.cleaned_data['password1'],)
            # login(request, new_user)
            # return redirect('editprofile')
            # return redirect('college')
        else:
          form = UserRegisterForm()
          messages.error(request, 'Username already exists in the Server. Please contact Admin')


            


    elif request.user.is_authenticated:
        print("heloooo babes")
        return redirect('index')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'sign-up.html', context)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

@csrf_exempt
def verify(request):
    if request.method == "POST":
        userotp = request.POST.get('otp')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        password = request.session.get('password')

        if Roll.objects.filter(roll=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # form = User(username=username, email=email, password = password)
            # form.save()

        print("OTP: ", userotp)
    return JsonResponse( {'data':'Hello'}, status=200)