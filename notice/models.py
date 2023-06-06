from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'


class Notice(models.Model):
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class Message(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_in = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
