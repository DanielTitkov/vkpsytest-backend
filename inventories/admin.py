from django.contrib import admin
from .models import Item, Scale, Inventory, Question, Response, Norm, Result, Sample, Progress



class ItemAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'author',
        'created',
        'updated',
    )



class ScaleAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'aggregation_method',
        'standart_scale',
        'normalization_method',
        # items - many-to-many - show count later
        'author', # maybe add link to author
        'created',
        'updated',
    )
    list_filter = (
        'aggregation_method',
        'standart_scale',
        'normalization_method',      
    )
    search_fields = (
        'title',
    )



class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'author', # maybe add link to author
        'created',
        'updated',
    )
    search_fields = (
        'title',
    )



class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'item',
        'scale',
        'question_type',
        'author', # maybe add link to author
        'created',
        'updated',
    )
    list_filter = (
        'question_type',      
    )
    search_fields = (
        # 'item__content',
        'scale__title',
    )



class ResponseAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'value',
        'item',
        'user', # link? 
        'question',
        'inventory',
        'created',
        'updated',
    )
    search_fields = (
        'inventory__title',
    )
    


class NormAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'scale',
        'sample',
        'norm_type',
        'values',
        'valid',
        'created',
        'updated',
    )
    list_filter = (
        'norm_type',
        'valid',    
    )
    search_fields = (
        # 'item__content',
        'scale__title',
        'sample__title',
    )



class ResultAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'value',
        'raw',
        'scale',
        'user', # link?
        'inventory',
        'created',
        'updated',
    )
    search_fields = (
        'scale__title',
        'inventory__title',
    )



class SampleAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'description',
        # 'age',
        'age_group',
        'sex',
        'city',
        'country',
        # 'timezone',
        'created',
        'updated',
    )
    list_filter = (
        'sex',
        'country',
        'age_group',    
    )
    search_fields = (
        "title",
    )



class ProgressAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user', # link
        'inventory',
        'status',
        'created',
        'updated',
    )
    list_filter = (
        'status',
    )
    search_fields = (
        'inventory__title',
    )



admin.site.register(Item, ItemAdmin)
admin.site.register(Scale, ScaleAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Norm, NormAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Progress, ProgressAdmin)




