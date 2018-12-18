from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Author(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=4000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RecipeItem(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=2000)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    time_required = models.CharField(max_length=50)
    instructions = models.TextField(max_length=2000)
    favorites = models.ManyToManyField(Author, related_name="author")

    def get_absolute_url(self):
        return reverse('homepage')

    def __str__(self):
        return self.title
