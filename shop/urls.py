from django.urls import path, include
from . import api

urlpatterns = [
  path('products', api.ListProductAPI.as_view(), name='products_list'),
  path('<int:category_id>/products', api.ListProductAPI.as_view(), name='products_by_category'),
  path('product/<int:pk>', api.DetailProductAPI.as_view(), name='product_detail'),
  path('categories', api.ListCategoryAPI.as_view(), name='list_category'),
]