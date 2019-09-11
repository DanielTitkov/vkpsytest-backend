from django.contrib import admin
from .models import MockUser, Item, Scale, Psytest, Question, Response

admin.site.register(MockUser)
admin.site.register(Item)
admin.site.register(Scale)
admin.site.register(Psytest)
admin.site.register(Question)
admin.site.register(Response)
