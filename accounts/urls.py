from django.urls import path, include
from .views import ProfileList

urlpatterns = [
    path('profile/', ProfileList.as_view())
]