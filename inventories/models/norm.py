from django.db import models
from django.contrib.postgres.fields import JSONField


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