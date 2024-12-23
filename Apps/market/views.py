from rest_framework import viewsets
from .serializers import PayMethodSerializer, BuyListSerializer, BuySerializer, ProductSerializer, StockSerializer, ProviderSerializer, CategorySerializer
from .models import PayMethod, Buy, BuyList, Provider, Product, Stock, Category
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

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

    def create(self, request, *args, **kwargs):
        pass

class StockViewSet(viewsets.ModelViewSet):
    """
        viewset para o estoque
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    @action(detail=False, methods=['get'], url_path='product/(?P<id>[^/.]+)', url_name='product')
    def list_estoque_product(self, request, *args, **kwargs):
        """
            funcao para listar o estoque de um produto
        """
        product = Product.objects.get(id=kwargs['id'])
        queryset = Stock.objects.filter(product=product)
        serializer = StockSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='category/(?P<id>[^/.]+)', url_name='category')
    def list_estoque_categories(self, request, *args, **kwargs):
        """
            funcao para listar o estoque de uma categoria
        """
        category = Category.objects.get(id=kwargs['id'])
        queryset = Stock.objects.filter(product__category=category)
        serializer = StockSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        """
            funcao para deletar um item do estoque
        """
        product = Product.objects.get(id=kwargs['id'])
        stock = Stock.objects.get(product=product)
        stock.delete()
        return Response({'message': 'Item deletado com sucesso!'}, status=status.HTTP_200_OK)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
