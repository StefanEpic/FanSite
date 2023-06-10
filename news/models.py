from django.contrib.auth.models import User
from django.db import models


class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class Subscribers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
