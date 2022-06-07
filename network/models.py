from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #Store primary keys of users you follow in a CSV, to check against later
    following = models.CharField(max_length=1000, null=True, blank=True)
    followcount = models.IntegerField(default=0)
    #Store pk's of liked chirps as a CSV
    likedchirps = models.CharField(max_length=1000, null=True, blank=True)

class Chirp(models.Model):
    chirp = models.CharField(max_length=280, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "chirp": self.chirp,
            "likes": self.likes,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "owner": self.owner.username
        }

    def __str__(self):
        return f"{self.chirp} by {self.owner} on {self.timestamp.strftime('%b %d %Y, at %I:%M %p')}"