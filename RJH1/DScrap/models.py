# Import necessary modules
from django.db import models

# Define your models
class TitleLink(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    image_url = models.URLField(default=None)
    relay1=models.CharField(max_length=255 , default="Couldnot Find the relay")
    relay2=models.CharField(max_length=255 , default="Couldnot Find the relay")
    relay3=models.CharField(max_length=255 , default="Couldnot Find the relay")
    timestamp = models.DateTimeField(auto_now_add=True)

class Title(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()

class Login(models.Model):
    Username = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)


    def __str__(self):
        return self.title
