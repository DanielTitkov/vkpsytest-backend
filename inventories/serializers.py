from rest_framework import serializers
from .models import MockUser, Item, Scale, Inventory, Question, Response, Norm, Sample



class MockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockUser
        fields = ("__all__")
        depth = 1



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
        fields = ("id", "item", "question_type")
        depth = 1


class InventorySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Inventory
        fields = ("__all__")
        # depth = 1


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ("__all__")
        depth = 1


class NormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Norm
        fields = ("__all__")
        depth = 1


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ("__all__")