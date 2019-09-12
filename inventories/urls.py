from django.urls import path, include
from rest_framework import routers
from .views import (
    ScaleView, InventoryView,
    ItemView, QuestionView,
    ResponseView, NormView,
    SampleView, MockUser
)

router = routers.DefaultRouter()
router.register("scales", ScaleView)
router.register("inventories", InventoryView)
router.register("items", ItemView)
router.register("questions", QuestionView)
router.register("responses", ResponseView)
router.register("norms", NormView)
router.register("samples", SampleView)
router.register("mockusers", MockUser)


urlpatterns = [
    path('', include(router.urls))
]