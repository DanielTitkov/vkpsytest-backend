from rest_framework import serializers
from .models import (
    Item, Scale, Inventory, Question, 
    Response, Norm, Sample, Result
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


class InventorySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Inventory
        fields = ("__all__")
        # depth = 1


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
    class Meta:
        model = Result
        fields = ("__all__")
