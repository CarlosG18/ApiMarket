from django.db import models
import uuid
from django.utils.timezone import now
from Apps.users.models import Provider, Client, Operator

class Category(models.Model):
    """
        model for create the category of products
    """
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return super().__str__()
    
class Product(models.Model):
    """
        model for create the product
    """
    name = models.CharField(max_length=200)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    mark = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return super().__str__()
    
class Stock(models.Model):
    """
        model for management of stock of products
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount_current = models.IntegerField()
    amount_min = models.IntegerField(blank=True)
    amount_max = models.IntegerField(blank=True)
    
    def __str__(self):
        return super().__str__()
    
class Alerts(models.Model):
    """
        model for create alerts for stock
    """
    TYPE_ALERT = [
        ('1', 'falta'),
        ('2', 'excesso'),
    ]

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=1, choices=TYPE_ALERT)
    message = models.TextField()
    
    def __str__(self):
        return super().__str__()


class BuyList(models.Model):
    """
        model for create buy list client's
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    day_buy = models.DateTimeField(default=now)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    amount_total = models.IntegerField(default=0)
    discount = models.FloatField(default=0.0)# value in % of amount total
    closed = models.BooleanField(default=False)
    
    def __str__(self):
        return super().__str__()

class Buy(models.Model):
    """
        model for create of a buy do on client
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="produtos")
    amount = models.IntegerField()
    price = models.FloatField()
    buylist = models.ForeignKey(BuyList, on_delete=models.CASCADE)
    
    def __str__(self):
        return super().__str__()
    
    
