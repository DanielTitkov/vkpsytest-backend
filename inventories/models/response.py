from django.db import models
from django.contrib.auth.models import User



class Response(models.Model):
    """
    Ответ указывает на то, какой ответ дал пользователь на конкретный пункт.
    А также дополнительные данные - типа когда это произошло и в какой тесте. 
    """
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE)
    value = models.FloatField() 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # limit choices

    class Meta:
        app_label = "inventories"

    def __str__(self): 
        return "Response to '{}' in '{}' by '{}'".format(
            self.item, self.inventory, self.user)