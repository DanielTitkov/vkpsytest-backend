from django.shortcuts import render
from rest_framework import viewsets
from .models import Item, Scale, Inventory, Question, Response, Norm, Sample
from .serializers import (
    ScaleSerializer, InventorySerializer, 
    ItemSerializer, QuestionSerializer, 
    ResponseSerializer, NormSerializer, 
    SampleSerializer
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
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer


class NormView(viewsets.ModelViewSet):
    queryset = Norm.objects.all()
    serializer_class = NormSerializer


class SampleView(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer