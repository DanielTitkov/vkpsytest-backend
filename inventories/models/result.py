from django.db import models
from django.contrib.auth.models import User



class Result(models.Model):
    """
    Результат связывает пользователя и шкалу.
    Вычисляется с помощью шкалы и нормы. 
    """
    scale = models.ForeignKey('Scale', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE)
    value = models.FloatField(blank=True)
    raw = models.FloatField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # limit choices

    class Meta:
        unique_together = ('scale', 'user',) 
        app_label = "inventories"

    def __str__(self):
        return "Result of user {} in '{}'".format(self.user, self.inventory)