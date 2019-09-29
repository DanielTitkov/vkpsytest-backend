from rest_framework import viewsets
from .models import Profile
from .serializers import ProfileSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class ProfileList(APIView):

    def get(self, request, format=None):
        user = self.request.user
        profile = Profile.objects.filter(user=user).first()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


    def post(self, request, format=None):
        user = self.request.user
        serializer = ProfileSerializer(data=request.data, context={'request': self.request})
        if serializer.is_valid(): 
            profile = Profile.objects.filter(user=user).first()
            if profile: # if profile exists - udpate, else create new
                if not Profile.is_new_data(profile, serializer.validated_data): 
                    # check if profile is really updated? If not, just return 
                    return Response(serializer.data, status=status.HTTP_200_OK)
                serializer.instance = profile # not sure if this is safe
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)