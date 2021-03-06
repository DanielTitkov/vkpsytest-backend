from typing import Optional
import statistics

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.conf import settings

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
        return "{}-norm for scale `{}` for sample `{}`".format(
            self.norm_type, self.scale, self.sample)

    
    @timing
    def recalculate(self):
        users = self.sample.users.all()
        results = Result.objects.filter(
            user__in=users,
            scale=self.scale,
        ).values("raw")
        results_raw_scores = [r.get('raw', 0) for r in results]
        if len(results_raw_scores) < settings.MIN_SAMPLE:
            return
        mean = statistics.mean(results_raw_scores)
        sd = statistics.stdev(results_raw_scores)
        self.values = {"mean": round(mean, 3), "sd": round(sd, 3)}
        self.save()

    
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