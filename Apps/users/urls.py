from .views import PayMethodViewSet, GerenteViewSet, OperatorViewSet, ProviderViewSet, PointViewSet, WorkDayViewSet, BatidaViewSet, EmployeeViewSet, ClientViewSet
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'paymethods', PayMethodViewSet, basename="patmethods")
router.register(r'gerentes', GerenteViewSet, basename='gerentes')
router.register(r'operators', OperatorViewSet, basename='operators')
router.register(r'providers', ProviderViewSet, basename='providers')
router.register(r'points', PointViewSet, basename='points')
router.register(r'workdays', WorkDayViewSet, basename='workdays')
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'employees', EmployeeViewSet, basename='employees')

urlpatterns = router.urls
