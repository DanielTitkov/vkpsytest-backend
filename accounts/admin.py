from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'age',
        'age_group',
        'sex',
        'city',
        'country',
        'created',
        'updated',
    )
    list_filter = (
        'sex',
        'city',
        'country',
        'age_group',   
    )

admin.site.register(Profile, ProfileAdmin)