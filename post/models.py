from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse
import uuid
from notification.models import Notification

CATEGORY_CHOICES = (
        ('Engg', 'Faculty of Engineering'),
        ('SC', 'Faculty of Science'),
        ('Comm', 'Faculty of Commerce'),
        ('Arts', 'Faculty of Arts'),
        ('Arch', 'Faculty of Architecture'),
        ('SS', 'Faculty of Social Science'),
        ('Ayush', 'Faculty of Ayush'),
        ('TC', 'Technical College'),
    )




# uploading user files to a specific directory
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Professor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path, verbose_name="Picture", null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    desig = models.CharField(max_length=100, null=True, blank=True)
    quali = models.CharField(max_length = 500, null=True, blank=True)
    facultyy = models.CharField(choices=CATEGORY_CHOICES, max_length=50, null=True, blank=True)
    phone = models.IntegerField(max_length = 15, null=True, blank=True)
    gmail =  models.EmailField(max_length = 254, null=True, blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True, default=uuid.uuid1)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

# class PostFileContent(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     file = models.FileField(upload_to=user_directory_path, verbose_name="Choose File")

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path, verbose_name="Picture")
    caption = models.CharField(max_length=10000, verbose_name="Caption")
    posted = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="tags")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("post-details", args=[str(self.id)])

    # def __str__(self):
    #     return str(self.caption)


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")

    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, user=post.user)
        notify.save()

    def user_unliked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification.objects.filter(post=post, sender=sender, notification_types=1)
        notify.delete()

# models.py
from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)  
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following
        notify = Notification(sender=sender, user=following, notification_types=3)
        notify.save()

    def user_unfollow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following
        notify = Notification.objects.filter(sender=sender, user=following, notification_types=3)
        notify.delete()

class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)

        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()


post_save.connect(Stream.add_post, sender=Post)

post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_unliked_post, sender=Likes)

post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)

STATUS = (
        ('Completed', 'Completed'),
        ('Ongoing', 'Ongoing'),
        ('Cancelled', 'Cancelled'),
        ('Waiting', 'Waiting'),
        ('Coming Soon', 'Coming Soon'),
        ('Postponed', 'Postponed'),
        ('Preponed', 'Preponed',),
        
    )

class Placement(models.Model):
    company = models.CharField(max_length=100)
    jd = models.FileField(upload_to="pdf", null=True, blank=True, default="no.jpg")
    branch = models.CharField(max_length=1000, null=True, blank=True)
    students_placed = models.CharField(max_length=10)
    status = models.CharField(choices=STATUS, max_length=50)
    year = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.company
    
class Student_Placed(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    package = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    batch = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


class Notes(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=10)
    course = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)
    link = models.FileField(upload_to="pdf", null=True, blank=True, default="no.jpg")


    def __str__(self):
        return self.subject_name


class Events(models.Model):
    title = models.CharField(max_length=100)
    date = models.CharField(max_length=10)
    description = models.CharField(max_length=100, null=True, blank=True)
    venue = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="profile_pciture", null=True, blank=True, default="no.jpg")

    def __str__(self):
        return self.title


class Alumni(models.Model):
    Name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="profile_pciture", null=True, blank=True, default="no.jpg")
    Batch = models.CharField(max_length=10)
    Course = models.CharField(max_length=10)
    Branch = models.CharField(max_length=10)
    Company = models.CharField(max_length=100, null=True, blank=True)
    Role = models.CharField(max_length=100, null=True, blank=True)
    linkedin = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.Name
    

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
