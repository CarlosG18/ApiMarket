from .views import PayMethodViewSet, GerenteViewSet, OperatorViewSet, ProviderViewSet, WorkDayViewSet, EmployeeViewSet, ClientViewSet, AdminViewSet, PointViewSet, BatidaViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'paymethods', PayMethodViewSet, basename="patmethods")
router.register(r'users/gerentes', GerenteViewSet, basename='gerentes')
router.register(r'users/operators', OperatorViewSet, basename='operators')
router.register(r'users/providers', ProviderViewSet, basename='providers')
router.register(r'workdays', WorkDayViewSet, basename='workdays')
router.register(r'users/clients', ClientViewSet, basename='clients')
router.register(r'users/employees', EmployeeViewSet, basename='employees')
router.register(r'users/admins', AdminViewSet, basename='admins')
router.register(r'points', PointViewSet, basename='points')
router.register(r'points/batidas', BatidaViewSet, basename='batidas')

urlpatterns = router.urls