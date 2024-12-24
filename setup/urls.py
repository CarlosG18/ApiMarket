from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from Apps.market.views import ProductViewSet, CategoryViewSet, StockViewSet, BuyListViewSet, BuyViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('buylists/<int:id>/', BuyListViewSet.as_view({'get': 'list', 'delete': 'destroy'})),
    path('buylists/', BuyListViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('buys/<int:id>/', BuyViewSet.as_view({'get': 'list', 'delete': 'destroy'})),
    path('buys/', BuyViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('products/<int:id>/', ProductViewSet.as_view({'get': 'list', 'delete': 'destroy'})),
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    #path('paymethods/<int:id>/', PayMethodViewSet.as_view({'get': 'list', 'delete': 'destroy'})),
    #path('paymethods/', PayMethodViewSet.as_view({'get': 'list', 'post': 'create'})),
    #path('providers/<int:id>/', ProviderViewSet.as_view({'get': 'list', 'delete': 'destroy'})),
    #path('providers/', ProviderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categorys/<int:id>/', CategoryViewSet.as_view({'get': 'list', 'delete': 'destroy'})),
    path('categorys/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    # url para o estoque
    path('stocks/', StockViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('stocks/product/<int:id>/', StockViewSet.as_view({'get': 'list_estoque_product', 'delete': 'destroy'})),
    path('stocks/product/<int:id>/add/', StockViewSet.as_view({'path': 'update'})),
    path('stocks/product/<int:id>/remove/', StockViewSet.as_view({'path': 'update'})),
    path('stocks/category/<int:id>/', StockViewSet.as_view({'get': 'list_estoque_categories'})),
    path('admin/', admin.site.urls),
    #path('api/', include('Apps.market.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', include('Apps.users.urls')),
]
