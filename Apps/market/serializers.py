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
        fields = '__all__'
        
class BuyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyList
        fields = '__all__'
        