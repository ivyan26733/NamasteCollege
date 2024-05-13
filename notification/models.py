from django.db import models
from django.contrib.auth.models import User
# from post.models import Post

class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Comment'), (3, 'Follow'))

    post = models.ForeignKey("post.Post", on_delete=models.CASCADE, related_name="notification_post", null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_from_user" )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_to_user" )
    notification_types = models.IntegerField(choices=NOTIFICATION_TYPES, null=True, blank=True)
    text_preview = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.text_preview

class Notif(models.Model):
    text = models.CharField(max_length=100, blank=True)
    FACULTY_CHOICES = [
        ('Engineering', 'Faculty of Engineering'),
        ('Science', 'Faculty of Science'),
        ('Arts', 'Faculty of Arts'),
        ('Arch', 'Faculty of Architecture'),
        ('Comm', 'Faculty of Commerce'),
        ('Ayush', 'Faculty of Integrated Alternative Medicine (AYUSH)'),
        ('SocialS', 'Faculty of Social Science'),
        ('Edu', 'Faculty of Education'),
        ('TC', 'Technical College'),

    ]
    faculty_m = models.CharField(max_length=100, choices=FACULTY_CHOICES, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)  # Add this line




from django.db import models
from django.contrib.auth.models import User

class DPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="profile_pciture", null=True, blank=True)
    content = models.TextField()
    dauthor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class DComment(models.Model):
    post = models.ForeignKey(DPost, related_name='comments', on_delete=models.CASCADE)
    dauthor = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
