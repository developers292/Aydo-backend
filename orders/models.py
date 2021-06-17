from django.db import models
from shop.models import Product
from decimal import Decimal
from django.conf import settings



class Province(models.Model):
    """ 
    Provinces that we can service orders to
    """
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def natural_key(self):
        return django_sub_dict(self) 
    


class City(models.Model):
    """
    Cities that we can service orders to
    """
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def natural_key(self):
        return django_sub_dict(self) 



class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    ref_code = models.CharField(max_length=50)
    province = models.ForeignKey(
        Province,
        related_name='this_province_orders',
        on_delete=models.SET_NULL,
        null=True
    )
    city = models.ForeignKey(
        City,
        related_name='this_city_orders',
        on_delete=models.SET_NULL,
        null=True
    )
    street = models.CharField(max_length=50)
    alley = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    detail_address = models.CharField(max_length=250)    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delivery_date = models.DateTimeField()
    paid = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    online_payment = models.BooleanField(default=True) # Fasle -> پرداخت در محل
    payment_verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-created',)


    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost



class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=15, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return str(self.id)
        
    def get_cost(self):
        return self.price * self.quantity