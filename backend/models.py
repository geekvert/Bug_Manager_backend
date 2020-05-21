from django.db import models
from djrichtextfield.models import RichTextField
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    enrollment_no = models.CharField(max_length=15, unique=True)
    admin_status = models.BooleanField(default=False)
    disabled_status = models.BooleanField(default=False)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class Project(models.Model):
    name = models.CharField(max_length=60)
    wiki = RichTextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator', on_delete=models.SET_NULL, null=True)
    team = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='team', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Bug(models.Model):
    heading = models.CharField(max_length=100)
    description = models.TextField()
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reported_by', on_delete=models.SET_NULL, null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_to', default=None, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, default=[])
    timestamp = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('P','pending'),
        ('R','resolved'),
        ('T','to_be_discussed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return self.heading

class Image(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'backend/bug_images/{Bug.heading}')

    def __str__(self):
        return self.image.name

class Comment(models.Model):
    body = models.TextField()
    buggy = models.ForeignKey(Bug, related_name='bug', on_delete=models.CASCADE)
    commentator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='commentator', on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:10]+'...'
