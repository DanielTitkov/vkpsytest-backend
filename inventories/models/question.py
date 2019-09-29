from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User



class Question(models.Model):
    """
    Вопрос связан с одним или несколькими пунктами. 
    Вопрос содержит логику представления пунктов - количество, тип шкалы и т.д. 
    """
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    scale = models.ForeignKey('Scale', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=10, default='likert', choices=[("likert", "likert"), ("fc", 'forced-choice')])
    display_options = JSONField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "inventories"


    def __str__(self):
        return "{} question with '{}' items".format(self.question_type, self.item)