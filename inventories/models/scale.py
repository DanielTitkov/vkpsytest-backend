from django.db import models
from django.contrib.auth.models import User

from .response import Response
from .result import Result
from .inventory import Inventory



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
    # items = models.ManyToManyField('Item', through='Question')
    # questions = models.ManyToManyField('Question')
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
        "T": lambda value: value * 10 + 50,
        "IQ": lambda value: value * 15 + 100,
    }

    class Meta:
        app_label = "inventories"


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
            question__scale=self, 
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

    
    @property
    def theoretical_norm(self) -> dict:
        print("RUNNING THEORETICAL NORM")
        norm_type = self.normalization_method
        if norm_type in ("NONE", "CTT"):
            questions = self.question_set.all()
            scale_min, scale_max = 0, 0
            for question in questions:
                scale_min += question.display_options.get('min')
                scale_max += question.display_options.get('max')
            mean_denominator = 2 if self.aggregation_method == "SUM" else 2 * questions.count()
            scale_mean = (scale_min + scale_max) / mean_denominator
    
            return {"mean": scale_mean, "sd": 0}
        return {}