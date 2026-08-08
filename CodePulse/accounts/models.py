from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class DeveloperProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    github_username = models.CharField(max_length=100, blank=True)
    github_id = models.CharField(max_length=100, blank=True)
    avatar_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    github_connected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username