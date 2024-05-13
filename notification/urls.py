from django.urls import path
from notification.views import ShowNotification, DeleteNotification
from . import views

urlpatterns = [
    path('', ShowNotification, name='show-notification'),
    path('<noti_id>/delete', DeleteNotification, name='delete-notification'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('all/', views.all_posts, name='all_posts'),
    path('notifs/', views.notif, name='notifs'),


]
