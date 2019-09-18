from django.shortcuts import render
from rest_framework import viewsets
from .models import (
    Item, Scale, Inventory, Question, 
    Response as ItemResponse, Norm, Sample, Result
)
from .serializers import (
    ScaleSerializer, InventorySerializer, 
    ItemSerializer, QuestionSerializer, 
    ResponseSerializer, NormSerializer, 
    SampleSerializer, ResultSerializer, ResultRequestSerializer
)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .mixins import CreateListMixin


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


class ResponseView(CreateListMixin, viewsets.ModelViewSet):
    serializer_class = ResponseSerializer

    def get_queryset(self):
        user = self.request.user
        return ItemResponse.objects.filter(user=user)


class NormView(viewsets.ModelViewSet):
    queryset = Norm.objects.all()
    serializer_class = NormSerializer


class SampleView(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer


class ResultList(APIView):

    def get(self, request, format=None):
        user = self.request.user
        results = Result.objects.filter(user=user)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        user = self.request.user
        request_serializer = ResultRequestSerializer(data=request.data)
        if request_serializer.is_valid(): # check if result is present 
            inventory = request_serializer.data.get("inventory")
            present_results = Result.objects.filter(user=user, inventory=inventory)
            if present_results.exists(): # if present - return
                result_serializer = ResultSerializer(present_results, many=True)
                return Response(result_serializer.data, status=status.HTTP_200_OK)
            else: # if not present - create and return
                scales = Scale.objects.filter(question__inventory=inventory).distinct() # get all scales for the test
                new_results = [s.calculate_result(user=user, inventory=inventory) for s in scales]
                result_serializer = ResultSerializer(new_results, many=True)
                return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)