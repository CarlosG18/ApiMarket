from rest_framework import routers
from .views import PayMethodViewSet, GerenteViewSet, OperatorViewSet, ProviderViewSet, PointViewSet, WorkDayViewSet

router = routers.DefaultRouter()
router.register(r'paymethods', PayMethodViewSet, basename="patmethods")
router.register(r'gerentes', GerenteViewSet, basename='gerentes')
router.register(r'operators', OperatorViewSet, basename='operators')
router.register(r'providers', ProviderViewSet, basename='providers')
router.register(r'points', PointViewSet, basename='points')
router.register(r'workdays', WorkDayViewSet, basename='workdays')

urlpatterns = router.urls
