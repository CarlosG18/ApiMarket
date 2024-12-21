from rest_framework import routers
from django.urls import path
from .views import ProductViewSet, PayMethodViewSet, ProviderViewSet, CategoryViewSet, StockViewSet, BuyListViewSet, BuyViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'paymethods', PayMethodViewSet, basename='paymethods')
router.register(r'providers', ProviderViewSet, basename='providers')
router.register(r'categorys', CategoryViewSet, basename='categorys')
router.register(r'stocks', StockViewSet, basename='stocks')
router.register(r'buys', BuyViewSet, basename='buys')
router.register(r'buylists', BuyListViewSet, basename='buylists')

urlpatterns = router.urls