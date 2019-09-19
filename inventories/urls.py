from django.urls import path, include
from rest_framework import routers
from .views import (
    ScaleView, InventoryView,
    ItemView, QuestionView,
    ResponseView, NormView,
    SampleView, 
    # ResultView,
    ResultList
)

router = routers.DefaultRouter()
router.register("scales", ScaleView)
router.register("inventories", InventoryView, basename="inventory")
router.register("items", ItemView)
router.register("questions", QuestionView)
router.register("responses", ResponseView, basename="response") 
router.register("norms", NormView)
router.register("samples", SampleView)
# router.register("results", ResultView, basename="result")



urlpatterns = [
    path('', include(router.urls)),
    path('results/', ResultList.as_view())
]