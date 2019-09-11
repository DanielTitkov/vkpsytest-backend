from django.db import models


class MockUser(models.Model):
    """
    Fake user model to test psytest relations. 
    Delete later. 
    """
    name = models.CharField(max_length=20)
    


class Item(models.Model):
    """
    Пункт - это структурная единица шкалы. Он содержит какой-то стимул. 
    """
    сontent = models.CharField(max_length=500)



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



class Psytest(models.Model):
    """
    Тест ничего не знает о шкалах и о компоновке вопросов.
    Он знает только том, какие вопросы в него включены.
    Тест содержит логику представления инструмента - инструкцию, сортировку и т.д. 
    """
    title = models.CharField(max_length=40)
    scales = models.ManyToManyField(Scale)
    description = models.CharField(max_length=500)
    instruction = models.CharField(max_length=500)
    author = models.ForeignKey(MockUser, on_delete=models.CASCADE) # mock user used



class Question(models.Model):
    """
    Вопрос связан с одним или несколькими пунктами. 
    Вопрос содержит логику представления пунктов - количество, тип шкалы и т.д. 
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=10, choices=[("likert", "likert"), ("fc", 'forced-choice')])



class Response(models.Model):
    """
    Ответ указывает на то, какой ответ дал пользователь на конкретный пункт.
    А также дополнительные данные - типа когда это произошло и в какой тесте. 
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(MockUser, on_delete=models.CASCADE) # mock user used
    value = models.FloatField() 



class Norm(models.Model):
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    group = models.CharField(max_length=50, default="ALL")



class Result(models.Model):
    """
    Результат связывает пользователя и тест. Он содержит значения по всем шкалам теста для пользователя.
    Вычисляется с помощью шкалы и нормы. 
    Можно использовать тут джейсон? 
    Или не пользователя и теста а пользователя и шкалу? Да, так логичнее, пожалуй. 
    """
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    user = models.ForeignKey(MockUser, on_delete=models.CASCADE) # mock user used
    value = models.FloatField()


