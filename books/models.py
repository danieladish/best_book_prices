from django.contrib.auth.models import User
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField()

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    favorite_books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.user.username
