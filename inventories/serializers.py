from rest_framework import serializers
from .models import (
    Item, Scale, Inventory, Question, 
    Response, Norm, Sample, Result, Progress
)



class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("__all__")



class ScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scale
        fields = ("__all__")
        depth = 1



class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "item", "question_type", "display_options")
        depth = 1


# class FooSerializer(serializers.ModelSerializer):
#   my_field = serializers.SerializerMethodField('is_named_bar')

#   def is_named_bar(self, foo):
#       return foo.name == "bar" 

#   class Meta:
#     model = Foo
#     fields = ('id', 'name', 'my_field')


class InventorySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField("get_questions")
    status = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = ("__all__")


    def get_status(self, obj):
        user = self.context.get("user")  
        return obj.get_status_for_user(user=user)

    
    def get_questions(self, obj):
        questions = obj.get_questions()
        serializer = QuestionSerializer(questions, many=True)
        return serializer.data



class ResponseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Response
        fields = ("__all__")
        depth = 0



class NormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Norm
        fields = ("__all__")
        depth = 1



class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ("__all__")



class ResultSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='scale.title', read_only=True)

    class Meta:
        model = Result
        fields = ("__all__")



class ResultRequestSerializer(serializers.Serializer):
    inventory = serializers.IntegerField()
