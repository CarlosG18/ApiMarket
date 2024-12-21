from rest_framework import viewsets
from .serializers import PayMethodSerializer, BuyListSerializer, BuySerializer, ProductSerializer, StockSerializer, ProviderSerializer, CategorySerializer
from .models import PayMethod, Buy, BuyList, Provider, Product, Stock, Category

# Create your views here.
class PayMethodViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = PayMethod.objects.all()
    serializer_class = PayMethodSerializer

class BuyViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Buy.objects.all()
    serializer_class = BuySerializer

class BuyListViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = BuyList.objects.all()
    serializer_class = BuyListSerializer

class ProviderViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class StockViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
