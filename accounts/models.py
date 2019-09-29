from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, default=None, blank=True)
    sex = models.CharField(max_length=10, null=True, default=None, blank=True)
    city = models.CharField(max_length=30, null=True, default=None, blank=True)
    country = models.CharField(max_length=30, null=True, default=None, blank=True)
    timezone = models.CharField(max_length=10, null=True, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} profile".format(self.user)
