from django.db import models
from base64 import b64encode

# Create your models here.
    
class Artist(models.Model):
    id=models.CharField(max_length=255, primary_key=True)
    name=models.CharField(max_length=255)
    age=models.IntegerField()
            

class Album(models.Model):
    id=models.CharField(max_length=255, primary_key=True)
    name=models.CharField(max_length=255)
    genre=models.CharField(max_length=255)
    artist_id=models.ForeignKey(Artist, on_delete=models.CASCADE)

class Track(models.Model):
    id=models.CharField(max_length=255, primary_key=True)
    name=models.CharField(max_length=255)
    duration=models.FloatField()
    times_played=models.IntegerField()
    album_id=models.ForeignKey(Album, on_delete=models.CASCADE)
