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
    AGGREGATION_METHODS = [
        ("SUM", "sum"),
        ("AVG", "average"),
    ]
    STANDART_SCALES = [
        ("STEN", "sten"),
        ("T", "tscore"),
        ("CUSTOM", "custom"),
        ("NONE", "none"), # that's acctually z-scores
    ]
    NORMALIZATION_METHODS = [
        ("CTT", "classical"),
        ("NONE", "none"), # keep raw scores
    ]

    title = models.CharField(max_length=40)
    description = models.CharField(max_length=500, blank=True)
    aggregation_method = models.CharField(max_length=10, choices=AGGREGATION_METHODS, default="AVG")
    standart_scale = models.CharField(max_length=10, choices=STANDART_SCALES, default="NONE")
    normalization_method = models.CharField(max_length=10, choices=NORMALIZATION_METHODS, default="NONE")
    items = models.ManyToManyField(Item, through='Question')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    aggregation_methods = {
        "SUM": lambda values: sum(values),
        "AVG": lambda values: sum(values)/len(values)
    }

    # this should be refactiored
    # it requires norm
    normalization_methods = {
        "NONE": lambda value, _: value,
        "CTT": lambda value, norm: (value-norm.values.get("mean"))/norm.values.get("sd"), # add defaults
    }

    # this should be refactiored
    standardization_methods = {
        "NONE": lambda value: value,
        "STEN": lambda value: value * 2 + 5.5, 
        "T": lambda valid: value * 10 + 50,
        "IQ": lambda valid: value * 15 + 100,
    }


    def __str__(self):
        return self.title


    def aggregate(self, values):
        return self.aggregation_methods[self.aggregation_method](values)


    def normalize(self, values, norm):
        return self.normalization_methods[self.normalization_method](values, norm)


    def standardize(self, values): 
        return self.standardization_methods[self.standart_scale](values)


    def calculate_result(self, user, inventory):
        # check user consistency? 
        responses = Response.objects.filter(
            item__scale=self, 
            user=user, 
            inventory=inventory
        ) # get all responses for scale items with user and inventory

        result_raw = self.aggregate([r.value for r in responses])
        result_value = result_raw

        if self.normalization_method != "NONE":  # standardization makes no sense if normalization is not applied
            norm = self.get_relevant_norm(user) 
            if norm: 
                result_value = self.standardize(self.normalize(result_raw, norm))
     
        result = Result(
            scale=self,
            user=user,
            inventory=Inventory(pk=inventory),
            value=result_value,
            raw=result_raw,
        )
        result.save()
        return result


    def get_relevant_norm(self, user):
        norm = Norm.objects.filter(
            sample__users=user,
            scale=self,
            valid=True,
            norm_type=self.normalization_method
        ).first()
        # probably need to degrade for more general norm here 
        # if norm is not present
        return norm



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
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    value = models.FloatField() 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # limit choices

    def __str__(self): 
        return "Response to '{}' in '{}' by '{}'".format(
            self.item, self.inventory, self.user)



class Sample(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True)
    users = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.title, self.description)



class Norm(models.Model):
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    norm_type = models.CharField(max_length=15, default="CTT")
    values = JSONField(default=dict)
    valid = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}-norm for scale `{}` for sample `{}`".format(
            self.norm_type, self.scale, self.sample)



class Result(models.Model):
    """
    Результат связывает пользователя и шкалу.
    Вычисляется с помощью шкалы и нормы. 
    """
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    value = models.FloatField()
    raw = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # limit choices

    def __str__(self):
        return "Result of user {} in '{}'".format(self.user, self.inventory)

