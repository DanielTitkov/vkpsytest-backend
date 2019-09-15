from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
 


class Item(models.Model):
    """
    Пункт - это структурная единица шкалы. Он содержит какой-то стимул. 
    """
    сontent = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.сontent



class Scale(models.Model):
    """
    Шкала - это совокупность пунктов, имеющая смысл с точки зрения предметной области.
    Шкала содержит логику подсчета результатов. 
    Соотносится с какой-то нормой и на выходе дает одно число на пользователя. 
    """
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=500)
    method = models.CharField(max_length=10, choices=[("sum", "sum"), ("avg", "average")], default="avg")
    items = models.ManyToManyField(Item, through='Question')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Question(models.Model):
    """
    Вопрос связан с одним или несколькими пунктами. 
    Вопрос содержит логику представления пунктов - количество, тип шкалы и т.д. 
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=10, default='likert', choices=[("likert", "likert"), ("fc", 'forced-choice')])
    display_options = JSONField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} question with '{}' items".format(self.question_type, self.item)



class Inventory(models.Model):
    """
    Тест ничего не знает о шкалах и о компоновке вопросов.
    Он знает только том, какие вопросы в него включены.
    Тест содержит логику представления инструмента - инструкцию, сортировку и т.д. 
    """
    title = models.CharField(max_length=40)
    questions = models.ManyToManyField(Question, blank=True)
    description = models.CharField(max_length=500, blank=True)
    details = models.CharField(max_length=500, blank=True)
    instruction = models.CharField(max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Response(models.Model):
    """
    Ответ указывает на то, какой ответ дал пользователь на конкретный пункт.
    А также дополнительные данные - типа когда это произошло и в какой тесте. 
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    value = models.FloatField() 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



class Sample(models.Model):
    title = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Norm(models.Model):
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    value = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



class Result(models.Model):
    """
    Результат связывает пользователя и тест. Он содержит значения по всем шкалам теста для пользователя.
    Вычисляется с помощью шкалы и нормы. 
    Можно использовать тут джейсон? 
    Или не пользователя и теста а пользователя и шкалу? Да, так логичнее, пожалуй. 
    """
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    value = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


