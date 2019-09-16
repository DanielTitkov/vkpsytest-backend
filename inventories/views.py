from django.shortcuts import render
from rest_framework import viewsets
from .models import (
    Item, Scale, Inventory, Question, 
    Response, Norm, Sample, Result
)
from .serializers import (
    ScaleSerializer, InventorySerializer, 
    ItemSerializer, QuestionSerializer, 
    ResponseSerializer, NormSerializer, 
    SampleSerializer, ResultSerializer
)


class ScaleView(viewsets.ModelViewSet):
    queryset = Scale.objects.all()
    serializer_class = ScaleSerializer


class InventoryView(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class ItemView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ResponseView(viewsets.ModelViewSet):
    serializer_class = ResponseSerializer

    def get_queryset(self):
        user = self.request.user
        return Response.objects.filter(user=user)


class NormView(viewsets.ModelViewSet):
    queryset = Norm.objects.all()
    serializer_class = NormSerializer


class SampleView(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer


class ResultView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResultSerializer

    def get_queryset(self):
        user = self.request.user
        return Result.objects.filter(user=user)
 