from django.urls import path, include
from . import api

urlpatterns = [
  path('products', api.ListProductAPI.as_view(), name='products_list'),
  path('product/<int:pk>', api.DetailProductAPI.as_view(), name='product_detail'),
]