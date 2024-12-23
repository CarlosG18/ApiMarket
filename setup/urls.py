from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from Apps.market.views import ProductViewSet, PayMethodViewSet, ProviderViewSet, CategoryViewSet, StockViewSet, BuyListViewSet, BuyViewSet

urlpatterns = [
    path('buylists/<int:id>/', BuyListViewSet.as_view({'get': 'list'})),
    path('buylists/', BuyListViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('buys/<int:id>/', BuyViewSet.as_view({'get': 'list'})),
    path('buys/', BuyViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('products/<int:id>/', ProductViewSet.as_view({'get': 'list'})),
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('paymethods/<int:id>/', PayMethodViewSet.as_view({'get': 'list'})),
    path('paymethods/', PayMethodViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('providers/<int:id>/', ProviderViewSet.as_view({'get': 'list'})),
    path('providers/', ProviderViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('categorys/<int:id>/', CategoryViewSet.as_view({'get': 'list'})),
    path('categorys/', CategoryViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('stocks/<int:id>/', StockViewSet.as_view({'get': 'list'})),
    path('stocks/', StockViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('admin/', admin.site.urls),
    #path('api/', include('Apps.market.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
