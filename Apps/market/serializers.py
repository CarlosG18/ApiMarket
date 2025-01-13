from rest_framework import serializers
from .models import Product, Category, Stock, Buy, BuyList
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
        
class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = ['product', 'amount', 'buylist']

    def validate(self, attrs):
        # validando se a quantidade de produtos é maior que 0
        if attrs['amount'] <= 0:
            raise serializers.ValidationError('Quantidade de produtos invalida')
        # validar se a quantidade esta disponivel no estoque
        product = attrs['product']
        stock = Stock.objects.get(product=product)
        if attrs['amount'] > stock.amount_current:
            raise serializers.ValidationError('Quantidade indisponivel no estoque, quantidade atual: {}'.format(stock.amount_current))
        
        # validar se a retirada da quantidade atual ficará menor que a quantidade minima
        if  stock.amount_current - attrs['amount'] < stock.amount_min:
            raise serializers.ValidationError('Quantidade menor que a quantidade minima, quantidade minima: {}'.format(stock.amount_min))
        
        return attrs
        
class BuyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyList
        fields = ['id', 'client', 'day_buy', 'amount_total', 'operator','closed','discount']
        