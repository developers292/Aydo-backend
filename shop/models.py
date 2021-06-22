from django.db import models
from django.urls import reverse
from .utils import django_sub_dict


class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=200,
        db_index=True
    )
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    




class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=200,
        db_index=True
    )
    slug = models.SlugField(
        max_length=200,
        db_index=True
    )
    main_image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=0)
    price_without_off = models.DecimalField(max_digits=15, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)
    show_price = models.BooleanField(default=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
    

    def __str__(self):
        return self.name




class AdditionalProductInfo(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='additional_info',
        on_delete=models.CASCADE
    )
    key = models.CharField(max_length=150)
    value = models.CharField(max_length=255)
    
    class Meta:
        unique_together = (('product','key'),)    

    def __str__(self):
        return str(self.id)
    
    

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True
    )

    def __str__(self):
        return self.product.name
    
    