from django.urls import path
from . import api

urlpatterns = [
  path(
    'category/create',
     api.CreateCategoryAPI.as_view(),
     name='create_category'
  ),
  path(
    'category/update-remove/<int:pk>',
     api.UpdateRemoveCategoryAPI.as_view(),
     name='update_remove_category'
  ),
  path(
    'product/create',
     api.CreateProductAPI.as_view(),
     name='create_product'
  ),
  path(
    'product/update-remove/<int:pk>',
     api.UpdateRemoveProductAPI.as_view(),
     name='update_remove_product'
  ),
  path(
    'product/additional-info/add/<int:pk>',
     api.AddProductAdditionalInfoAPI.as_view(),
     name='add_additional_info'
  ),
  path(
    'product/additional-info/update-remove/<int:pk>',
     api.UpdateRemoveProductAdditionalInfoAPI.as_view(), 
     name='update_remove_additional_info'
  ),
  path(
    'product/image/add/<int:pk>',
     api.AddProductImageAPI.as_view(),
     name='add_image_product'
  ),
  path(
    'product/image/remove/<int:pk>',
     api.RemoveProductImageAPI.as_view(),
     name='remove_product_image'
  ),
]