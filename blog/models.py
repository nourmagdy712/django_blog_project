from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    created_date = models.DateTimeField(default=timezone.now)  # Automatically set when created
    published_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title