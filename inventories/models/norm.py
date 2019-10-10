from typing import Optional
import statistics

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

from .result import Result
from .scale import Scale

from vkpsytest.utils import timing



class Norm(models.Model):
    NORM_TYPES = [
        ("CTT", "Classical Test Theory"),
    ]
    scale = models.ForeignKey('Scale', on_delete=models.CASCADE)
    sample = models.ForeignKey('Sample', on_delete=models.CASCADE)
    norm_type = models.CharField(max_length=15, choices=NORM_TYPES, default="CTT") # add choices!!
    values = JSONField(default=dict)
    valid = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sample', 'scale', 'norm_type',)
        app_label = "inventories"


    def __str__(self):
        print("RECALCULATING")
        self.recalculate()
        return "{}-norm for scale `{}` for sample `{}`".format(
            self.norm_type, self.scale, self.sample)

    
    @timing
    def recalculate(self):
        users = self.sample.users.all()
        results = Result.objects.filter(
            user__in=users,
            scale=self.scale,
        ).values("raw")
        print(results)
        results_raw_scores = [r.get('raw', 0) for r in results]
        mean = statistics.mean(results_raw_scores)
        sd = 1 if len(results_raw_scores) < 2 else statistics.stdev(results_raw_scores)
        print(mean, sd)

    
    @classmethod
    def recalculate_all_norms(
        cls, 
        user: Optional[User] = None, 
        scale: Optional[Scale] = None, 
        result: Optional[Result] = None
    ):
        if result:
            user = result.user
            scale = result.scale
        if user and scale: # recalculate for particular result
            pass
        else: # recalculate all
            norms = cls.objects.all()
            for norm in norms:
                norm.recalculate()
        pass