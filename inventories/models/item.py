from django.db import models
from django.contrib.auth.models import User
 


class Item(models.Model):
    """
    Пункт - это структурная единица шкалы. Он содержит какой-то стимул. 
    """
    content = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "inventories"


    def __str__(self):
        return self.content