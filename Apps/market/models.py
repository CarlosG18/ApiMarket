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
    amount_min = models.IntegerField()
    amount_max = models.IntegerField()
    
    def __str__(self):
        return super().__str__()
    
class Buy(models.Model):
    """
        model for create of a buy do on client
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.FloatField()
    
    def __str__(self):
        return super().__str__()
    
class BuyList(models.Model):
    """
        model for create buy list client's
    """
    products = models.ManyToManyField(Product)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    day_buy = models.DateTimeField(default=now)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    amount_total = models.IntegerField()
    discount = models.IntegerField()# value in % of amount total
    
    def __str__(self):
        return super().__str__()
    
