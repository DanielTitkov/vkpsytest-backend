from django.db import models



class Psytest(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title



class Scale(models.Model):

    def __str__(self):
        return self.title



class Question(models.Model):
    question_type = models.CharField(max_length=10, choices=["likert", 'forced-choice'])

    def __str__(self):
        return self.title



class Item(models.Model):
    сontent = models.CharField(max_length=500)

    def __str__(self):
        return self.title