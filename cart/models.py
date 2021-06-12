from django.db import models
from shop.models import Product
from django.conf import settings

class Cart(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    owner =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='cart',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()


    def __str__(self):
        return str(self.id)
    
    def get_total_price(self):
        return quantity * product.price
    

