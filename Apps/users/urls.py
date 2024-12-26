from rest_framework import routers
from .views import PayMethodViewSet, GerenteViewSet, OperatorViewSet, ProviderViewSet, PointViewSet, WorkDayViewSet, BatidaViewSet
from django.urls import path

router = routers.DefaultRouter()
router.register(r'paymethods', PayMethodViewSet, basename="patmethods")
router.register(r'gerentes', GerenteViewSet, basename='gerentes')
router.register(r'operators', OperatorViewSet, basename='operators')
router.register(r'providers', ProviderViewSet, basename='providers')

urlpatterns = router.urls
