from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
from post.models import Post

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pciture", null=True, default="default.jpg")
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    favourite = models.ManyToManyField(Post, blank=True)

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
    faculty = models.CharField(max_length=100, choices=FACULTY_CHOICES, null=True, blank=True)

    COURSE_CHOICES = [
        ('B.Tech', 'B.Tech'),
        ('B.Sc', 'B.Sc'),
        ('B.A', 'B.A'),
        ('M.Tech', 'M.Tech'),
    ]
    course = models.CharField(max_length=20, choices=COURSE_CHOICES, null=True, blank=True)

    BRANCH_CHOICES = [
        ('ME', 'ME'),
        ('EE', 'EE'),
        ('physics', 'Physics'),
        ('English', 'English'),
    ]
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES, null=True, blank=True)

    YEAR_CHOICES = [
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
    ]
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f'{self.user.username} - Profile'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


class Roll(models.Model):
    roll = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return self.roll
    

from django.db import models


