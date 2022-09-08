from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=20)
    audience = models.IntegerField()
    release_date = models.DateField()
    genre = models.TextField()
    score = models.FloatField()
    poster_url = models.TextField()
    description = models.TextField()
    

