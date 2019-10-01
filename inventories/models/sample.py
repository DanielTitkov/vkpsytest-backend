import itertools
from django.db import models
from django.contrib.auth.models import User


def generate_age_groups(spec):
    groups = []
    first, last = 0, len(spec)-1
    for i, interval in enumerate(spec):
        desc = "{}{}{}".format(
            interval[0] if i is not first else "Less than",
            " " if i in [first, last] else "-",
            interval[1] if i is not last else "and more",
        )
        groups.append((str(i+1), desc))
    return groups



class Sample(models.Model):
    AGE_GROUPS_SPEC = [
        (0, 18),   # 1
        (18, 21),  # 2
        (22, 25),  # 3
        (26, 29),  # 4
        (30, 34),  # 5
        (35, 39),  # 6
        (40, 49),  # 7
        (50, 59),  # 8
        (60, 70),  # 9
        (70, 200), # 10
    ]
    AGE_GROUPS = generate_age_groups(AGE_GROUPS_SPEC)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True, default="")
    users = models.ManyToManyField(User)
    age = models.IntegerField(null=True, default=None, blank=True)
    age_group = models.CharField(max_length=20, null=True, default=None, blank=True, choices=AGE_GROUPS)
    sex = models.CharField(max_length=10, null=True, default=None, blank=True)
    city = models.CharField(max_length=30, null=True, default=None, blank=True)
    country = models.CharField(max_length=30, null=True, default=None, blank=True)
    timezone = models.CharField(max_length=10, null=True, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    sample_fields = ['sex', 'age_group', 'city', 'country']
    sample_fields_fall_through = ['city']

    class Meta:
        unique_together = ('sex', 'age_group', 'city', 'country',) # copy paste here... :(
        app_label = "inventories"


    def __str__(self):
        return self.title


    @classmethod
    def define_age_group(cls, age):
        for i, interval in enumerate(cls.AGE_GROUPS_SPEC):
            if age in range(interval[0], interval[1]+1):
                return i+1
        return None


    @classmethod
    def generate_sample_title(cls, spec):
        title_struct = [str(spec.get(f) or "all") for f in cls.sample_fields]
        return "-".join(title_struct)


    @classmethod
    def generate_sample_description(cls, spec):
        title_struct = []
        for field in cls.sample_fields:
            title_struct.append("{}:{}".format(
                field, 
                spec.get(field) or "all",
            ))
        return ";".join(title_struct)


    @classmethod
    def generate_sample_specs_for_user(cls, profile):
        """
        Generates unique sample specifications based on user profile
        socio-demographic data
        """
        combinations = []
        for i in range(0, len(cls.sample_fields)+1):
            combinations += itertools.combinations(cls.sample_fields, i)
        samples = []
        for combination in combinations:
            if combination and not combination[-1] in cls.sample_fields_fall_through:
                samples.append({
                    k:(getattr(profile, k, None) if k in combination else None)
                    for k in cls.sample_fields
                })
        return [dict(p) for p in set(tuple(i.items()) for i in samples)]


    @classmethod
    def generate_samples_for_user(cls, user):
        user.sample_set.clear() # clear old samples; this seems cheaper than process each sample
        for spec in cls.generate_sample_specs_for_user(user.profile):
            sample = cls.objects.filter(**spec).first()
            if not sample: # if sample doesn't exist - create new
                sample = cls(
                    title=cls.generate_sample_title(spec),
                    description=cls.generate_sample_description(spec),
                    **spec
                )
                sample.save()
            sample.users.add(user)