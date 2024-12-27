from rest_framework import viewsets
from .serializers import BuyListSerializer, BuySerializer, ProductSerializer, StockSerializer, CategorySerializer
from .models import Buy, BuyList, Product, Stock, Category
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

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

class ProductViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class StockViewSet(viewsets.ModelViewSet):
    """
        viewset para o estoque
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']

    def list_estoque_product(self, request, *args, **kwargs):
        """
            funcao para listar o estoque de um produto
        """
        product = Product.objects.get(id=kwargs['id'])
        queryset = Stock.objects.filter(product=product)
        serializer = StockSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    
    def update(self, request, *args, **kwargs):
        """
            funcao para atualizar o estoque
        """
        product = request.data['product']
        stock = Stock.objects.get(product=product)
        if 'amount_current' in request.data:
            stock.amount_current = request.data['amount_current']
        if 'amount_min' in request.data:
            stock.amount_min = request.data['amount_min']
        if 'amount_max' in request.data:
            stock.amount_max = request.data['amount_max']
        stock.save()
        return Response({'message': 'Estoque atualizado com sucesso!'}, status=status.HTTP_200_OK)
    
    def get_info_stock(self, request, *args, **kwargs):
        """
            funcao para pegar as informacoes gerais do estoque
        """
        data_stock = {
            'amunt_current': 0,
            'amount_min': 0,
            'amount_max': 0
        }

        for stock in Stock.objects.all():
            data_stock['amunt_current'] += stock.amount_current
            data_stock['amount_min'] += stock.amount_min
            data_stock['amount_max'] += stock.amount_max

        return Response(data_stock, status=status.HTTP_200_OK)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
