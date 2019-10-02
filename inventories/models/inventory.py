from django.db import models
from django.contrib.auth.models import User

from .progress import Progress
from .question import Question



class Inventory(models.Model):
    """
    Тест ничего не знает о шкалах и о компоновке вопросов.
    Он знает только том, какие вопросы в него включены.
    Тест содержит логику представления инструмента - инструкцию, сортировку и т.д. 
    """
    title = models.CharField(max_length=40)
    # questions = models.ManyToManyField('inventories.Question', blank=True) ###
    scales = models.ManyToManyField('Scale', blank=True)
    user = models.ManyToManyField(User, through='Progress')
    description = models.CharField(max_length=500, blank=True)
    details = models.CharField(max_length=500, blank=True)
    instruction = models.CharField(max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "inventories"
        

    def __str__(self):
        return self.title

    
    def get_status_for_user(self, user):
        if user:   
            progress_set = Progress.objects.filter(user=user, inventory=self.id)
            if progress_set.exists() and len(progress_set) == 1:
                progress = progress_set.first()
                return progress.status.lower()
        return None

    
    def get_questions(self):
        scales = self.scales.all()
        print(scales)
        questions = Question.objects.filter(scale__in=scales).all()
        print(questions)
        # return
        return questions