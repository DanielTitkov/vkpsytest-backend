from django.contrib import admin
from .models import MockUser, Item, Scale, Inventory, Question, Response, Norm

admin.site.register(MockUser)
admin.site.register(Item)
admin.site.register(Scale)
admin.site.register(Inventory)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Norm)

