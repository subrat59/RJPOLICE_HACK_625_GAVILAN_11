# Import necessary modules
from django.db import models

# Define your models
class TitleLink(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    image_url = models.URLField(default=None)
    timestamp = models.DateTimeField(auto_now_add=True)

class Title(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()


    def __str__(self):
        return self.title
