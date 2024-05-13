# import imp
from django.shortcuts import render, redirect
from notification.models import Notification

def ShowNotification(request):
    # user = request.user
    # notifications = Notification.objects.filter(user=user).order_by('-date')
    faculty = request.user.profile.faculty

    # Filter notifications based on the faculty associated with the user's profile
    notifications = Notif.objects.filter(faculty_m=faculty)

    context = {
        'notifications': notifications,

    }
    return render(request, 'notifications/notification.html', context)

def DeleteNotification(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, user=user).delete()
    return redirect('show-notification')

from django.shortcuts import render, redirect
from .models import DPost, DComment
from .forms import PostForm, CommentForm

def post_detail(request, post_id):
    post = DPost.objects.get(id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.dauthor = request.user
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.dauthor = request.user
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


from django.shortcuts import render
from .models import DPost, Notif

def all_posts(request):
    posts = DPost.objects.all()
    return render(request, 'all_posts.html', {'posts': posts})


def notif(request):
    faculty = request.user.profile.faculty

    # Filter notifications based on the faculty associated with the user's profile
    notifs = Notif.objects.filter(faculty_m=faculty)
    # notifs = Notif.objects.all()
    return render(request, 'notifications/notif.html', {'notifs':notifs})