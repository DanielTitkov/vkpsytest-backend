import itertools
from django.db import models
from django.contrib.auth.models import User



class Sample(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True, default="")
    users = models.ManyToManyField(User)
    age = models.IntegerField(null=True, default=None, blank=True)
    sex = models.CharField(max_length=10, null=True, default=None, blank=True)
    city = models.CharField(max_length=30, null=True, default=None, blank=True)
    country = models.CharField(max_length=30, null=True, default=None, blank=True)
    timezone = models.CharField(max_length=10, null=True, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    sample_fields = ['sex', 'age', 'city', 'country']

    class Meta:
        unique_together = ('sex', 'age', 'city', 'country',) # copy paste here... :(
        app_label = "inventories"


    def __str__(self):
        return self.title


    def generate_sample_title(self, spec):
        title_struct = [str(spec.get(f) or "all") for f in self.sample_fields]
        return "-".join(title_struct)


    def generate_sample_description(self, spec):
        title_struct = []
        for field in self.sample_fields:
            title_struct.append("{}:{}".format(
                field, 
                spec.get(field) or "all",
            ))
        return ";".join(title_struct)


    def generate_sample_specs_for_user(self, profile):
        """
        Generates unique sample specifications based on user profile
        socio-demographic data
        """
        combinations = []
        for i in range(0, len(self.sample_fields)+1):
            combinations += itertools.combinations(self.sample_fields, i)
        samples = []
        for combination in combinations:
            samples.append({
                k:(getattr(profile, k, None) if k in combination else None)
                for k in self.sample_fields
            })
        return [dict(p) for p in set(tuple(i.items()) for i in samples)]


    def generate_samples_for_user(self, user):
        user.sample_set.clear() # clear old samples; this seems cheaper than process each sample
        for spec in self.generate_sample_specs_for_user(user.profile):
            sample = Sample.objects.filter(**spec).first()
            if not sample: # if sample doesn't exist - create new
                sample = Sample(
                    title=self.generate_sample_title(spec),
                    description=self.generate_sample_description(spec),
                    **spec
                )
                sample.save()
            sample.users.add(user)