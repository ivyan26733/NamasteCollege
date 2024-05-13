from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

from post.models import Post, Tag, Follow, Stream, Likes, Professor
from django.contrib.auth.models import User
from post.forms import NewPostform
from authy.models import Profile
from django.urls import resolve
from comment.models import Comment
from comment.forms import NewCommentForm
from django.core.paginator import Paginator
from notification.models import Notif

from django.db.models import Q
# from post.models import Post, Follow, Stream
from django.shortcuts import render, redirect
from .forms import FeedbackForm


def home(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Check if the user-agent contains any keyword indicating mobile or tablet
    if 'Mobile' in user_agent or 'Tablet' in user_agent:
        # Redirect to a page indicating that the site is only accessible from a desktop
        return redirect('desktop_only_page')
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to a 'thank you' page (you'll need to create this)
    else:
        form = FeedbackForm()
    return render(request, 'home.html', {'form':form})

def professors(request):
   Engg = Professor.objects.filter(facultyy='Engg')
   return render(request, 'Professors.html',{'Engg':Engg})

def engg_professor(request):
   Engg = Professor.objects.filter(facultyy='Engg')
   return render(request, 'Engg_Prof.html',{'Engg':Engg})

def sc_professor(request):
   Enggs = Professor.objects.filter(facultyy='SC')
#    print(Enggs)
   return render(request, 'Sc_Prof.html',{'Enggs':Enggs})

def comm_professor(request):
   Enggs = Professor.objects.filter(facultyy='Comm')
#    print(Enggs)
   return render(request, 'Comm_Prof.html',{'Enggs':Enggs})

def arts_professor(request):
   Enggs = Professor.objects.filter(facultyy='Arts')
#    print(Enggs)
   return render(request, 'Arts_Prof.html',{'Enggs':Enggs})

def arch_professor(request):
   Enggs = Professor.objects.filter(facultyy='Arch')
#    print(Enggs)
   return render(request, 'Arch_Prof.html',{'Enggs':Enggs})

def ss_professor(request):
   Enggs = Professor.objects.filter(facultyy='SS')
#    print(Enggs)
   return render(request, 'SS_Prof.html',{'Enggs':Enggs})

def ayush_professor(request):
   Enggs = Professor.objects.filter(facultyy='Ayush')
#    print(Enggs)
   return render(request, 'Ayush_Prof.html',{'Enggs':Enggs})

def tc_professor(request):
   Enggs = Professor.objects.filter(facultyy='TC')
#    print(Enggs)
   return render(request, 'TC_Prof.html',{'Enggs':Enggs})

@login_required
def index(request):
    user = request.user
    user = request.user
    all_users = User.objects.all()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    profile = Profile.objects.all()

    posts = Stream.objects.filter(user=user)
    group_ids = []

    faculty = request.user.profile.faculty

    # Filter notifications based on the faculty associated with the user's profile
    notifs = Notif.objects.filter(faculty_m=faculty)

    
    for post in posts:
        group_ids.append(post.post_id)
        
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(username__icontains=query))

        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)


    context = {
        'post_items': post_items,
        'follow_status': follow_status,
        'profile': profile,
        'all_users': all_users,
        'notifs':notifs
        # 'users_paginator': users_paginator,
    }
    return render(request, 'index.html', context)


@login_required
def NewPost(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    tags_obj = []
    
    if request.method == "POST":
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')
            tag_list = list(tag_form.split(','))

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            p.tags.set(tags_obj)
            p.save()
            return redirect('profile', request.user.username)
    else:
        form = NewPostform()
    context = {
        'form': form
    }
    return render(request, 'newpost.html', context)

@login_required
def PostDetail(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post-details', args=[post.id]))
    else:
        form = NewCommentForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments
    }

    return render(request, 'postdetail.html', context)

@login_required
def Tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    context = {
        'posts': posts,
        'tag': tag

    }
    return render(request, 'tag.html', context)


# Like function
@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
        
    post.likes = current_likes
    post.save()
    # return HttpResponseRedirect(reverse('post-details', args=[post_id]))
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))

@login_required
def favourite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))

from .models import Professor

def college(request):
    return render(request, 'Colleges_name.html')

from .models import Placement

from django.shortcuts import render
from .models import Placement

from django.shortcuts import render
from .models import Placement
from django.db.models import Count, Sum

from django.shortcuts import render
from .models import Placement
from django.db.models import Count, Sum

def placement(request):
    place = Placement.objects.all()

    # Filter placements based on selected year
    selected_year = request.GET.get('year')
    if selected_year:
        place = place.filter(year=selected_year)

    # Calculate total number of companies and total number of students for each year
    years_data = Placement.objects.values('year').annotate(
        total_companies=Count('company', distinct=True),
        total_students=Sum('students_placed', default=0)
    )

    # Filter years_data based on the selected year
    if selected_year:
        years_data = years_data.filter(year=selected_year)
    else:
        years_data = None

    return render(request, 'placement.html', {'place': place, 'years_data': years_data})


from .models import Student_Placed
def student_placed(request):
    student = Student_Placed.objects.all()

    return render(request, 'students_placed.html', {'student': student})

from .models import Notes
def faculty_notes(request):
    notes = Notes.objects.all()

    return render(request, 'faculty_notes.html', {'notes':notes})

from .models import Events

from datetime import datetime
from django.utils import timezone

def events(request):
    current_date = timezone.now().date()
    upcoming_events = Events.objects.filter(date__gte=current_date.strftime('%Y-%m-%d'))
    past_events = Events.objects.filter(date__lt=current_date.strftime('%Y-%m-%d'))

    return render(request, 'events.html', {'upcoming_events': upcoming_events, 'past_events': past_events})


from django.shortcuts import render
from .models import Events

def archives_view(request):
    current_date = timezone.now().date()
    past_events = Events.objects.filter(date__lt=current_date.strftime('%Y-%m-%d'))
    return render(request, 'archives.html', {'past_events': past_events})


from .models import Alumni


# def alumni(request):
#     alumni = Alumni.objects.all()

#     return render(request, 'alumni.html', {'alumni':alumni})

from django.shortcuts import render
from .models import Alumni
from .forms import AlumniFilterForm

def alumni(request):
    alumni = Alumni.objects.all()
    filtered_alumni = None

    if request.method == 'POST':
        form = AlumniFilterForm(request.POST)
        if form.is_valid():
            batch = form.cleaned_data.get('batch')
            course = form.cleaned_data.get('course')
            branch = form.cleaned_data.get('branch')
            company = form.cleaned_data.get('company')
            role = form.cleaned_data.get('role')

            # Filter alumni based on form data
            filtered_alumni = Alumni.objects.filter(
                Batch__icontains=batch,
                Course__icontains=course,
                Branch__icontains=branch,
                Company__icontains=company,
                Role__icontains=role
            )
    else:
        form = AlumniFilterForm()

    return render(request, 'alumni.html', {'alumni': alumni, 'form': form, 'filtered_alumni': filtered_alumni})


def contact(request):

    return render(request, 'contact.html')

def contact2(request):

    return render(request, 'contact2.html')

def gallery(request):
    # alumni = Alumni.objects.all()

    return render(request, 'gallery.html')


# views.py
from django.shortcuts import redirect
from .models import Report

def save_post_text(request, post_id):
    if request.method == 'POST':
        post_text = request.POST.get('post_text')
        post = Post.objects.get(pk=post_id)  # Replace 'YourPostModel' with your actual post model
        Report.objects.create(post=post, text=post_text)
    return redirect('index')  # Replace 'your_redirect_url' with the URL you want to redirect after form submission



# views.py

from django.shortcuts import redirect, render



def desktop_only_page(request):
    # Render a page indicating that the site is only accessible from a desktop
    return render(request, 'desktop_only.html')
