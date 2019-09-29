from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User



class Progress(models.Model):
    STATUSES = [
        ("NS", "Not started"),
        ("PROGRESS", "In progress"),
        ("DONE", "Done"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE)
    data = JSONField(default=dict, blank=True)
    status = models.CharField(max_length=10, default="NS", choices=STATUSES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'inventory',)
        app_label = "inventories"


    def __str__(self):
        return "Progress of {} in {}".format(self.user, self.inventory)