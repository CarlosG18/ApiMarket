from rest_framework import viewsets, filters
from .serializers import BuyListSerializer, BuySerializer, ProductSerializer, StockSerializer, CategorySerializer
from .models import Buy, BuyList, Product, Stock, Category
from Apps.users.models import Client
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from Apps.users.permissions import IsRoleUser

class BuyViewSet(viewsets.ModelViewSet):
    """
        
    """
    queryset = Buy.objects.all()
    serializer_class = BuySerializer
    required_roles = ['operator', 'Admin']
    permission_classes = [IsRoleUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        product = Product.objects.get(id=request.data['product'])

        if serializer.is_valid():
            price = product.price * request.data['amount']
            serializer.save(price=price)
            # atualizar o estoque
            stock = Stock.objects.get(product=product)
            stock.amount_current -= request.data['amount']
            stock.save()
            # atualizar a buylist
            buylist = BuyList.objects.get(id=request.data['buylist'])
            buylist.amount_total += price
            buylist.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BuyListViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = BuyList.objects.all().order_by('id')
    serializer_class = BuyListSerializer
    filter_backends = (DjangoFilterBackend,filters.OrderingFilter)
    ordering_fields = ('client', 'data_buy')
    required_roles = ['operator', 'Admin']
    permission_classes = [IsRoleUser]

    def list_products(self, request, *args, **kwargs):
        buylist = BuyList.objects.get(id=kwargs['id'])
        buys = Buy.objects.filter(buylist=buylist)
        products = [buy.product for buy in buys]

        data_response = {}
        for index, buy in enumerate(set(buys)):
            data_response[f'produto_{index}'] = {
                'produto': buy.product.name,
                'preço_produto': buy.product.price,
                'preço_total': buy.price,
                'quantidade': buy.amount,

            }       
        return Response(data_response, status=status.HTTP_200_OK)
    
    def list_buylist_client(self, request, *args, **kwargs):
        try:
            client = get_object_or_404(Client, id=kwargs['id'])
        except:
            return Response({'message': 'client with specified id does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        buylist = BuyList.objects.filter(client=client)
        serializer = self.get_serializer(buylist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    required_roles = ['Provider', 'Admin']
    permission_classes = [IsRoleUser]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class StockViewSet(viewsets.ModelViewSet):
    """
        viewset para o estoque
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    required_roles = ['Gerente', 'Admin']
    permission_classes = [IsRoleUser]
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
    required_roles = ['Provider', 'Admin']
    permission_classes = [IsRoleUser]
