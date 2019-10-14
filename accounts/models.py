from django.db import models
from django.contrib.auth.models import User

from inventories.models import Sample
from inventories.models import Norm
from inventories.models import Scale

from vkpsytest.utils import timing


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, default=None, blank=True)
    age_group = models.CharField(max_length=20, null=True, default=None, blank=True, choices=Sample.AGE_GROUPS)
    sex = models.CharField(max_length=10, null=True, default=None, blank=True)
    city = models.CharField(max_length=30, null=True, default=None, blank=True)
    country = models.CharField(max_length=30, null=True, default=None, blank=True)
    timezone = models.CharField(max_length=10, null=True, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):

        print("GETTING NORM")
        scale = Scale.objects.filter(title="Stupid scale").first()
        self.get_optimal_norm(scale)

        return "{} profile".format(self.user)


    def save(self, *args, **kwargs):
        """
        Redifined save method to use instead of signal, because singnals lead to noodle code.
        On profile create or update user samples are recalculated.
        Maybe add extensive logging later.
        """
        self.age_group = Sample.define_age_group(self.age) 
        super().save(*args, **kwargs)  # Call the "real" save() method.
        Sample.generate_samples_for_user(self.user) # this is long Sample method


    @timing
    def get_optimal_norm(self, scale: Scale) -> Norm:
        norm = Norm.objects.filter(
            sample__users=self.user,
            scale=scale,
            valid=True,
            norm_type=scale.normalization_method
        ).first()
        # probably need to degrade for more general norm here 
        # if norm is not present - create new norm? 
        print(self.user)
        print(scale, scale.normalization_method)
        print(norm)
        return norm


    def update_norms(self, scale: Scale):
        norms = Norm.objects.filter(
            sample__users=self.user,
            scale=scale,
            valid=True,
            norm_type=scale.normalization_method
        ).all()
        for norm in norms:
            norm.recalculate()


    @staticmethod
    def is_new_data(obj, data): # this should be actually put in separate library
        for k, v in data.items():
            if getattr(obj, k, None) != v:
                return True
        return False
