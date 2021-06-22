from django.urls import path
from . import api

urlpatterns = [
  path('category/create', api.CreateCategoryAPI.as_view(), name='create_category'),
  path('category/update-remove/<int:pk>', api.UpdateRemoveCategoryAPI.as_view(), name='update_remove_category'),
  path('product/create', api.CreateProductAPI.as_view(), name='create_product'),
  path('product/update-remove/<int:pk>', api.UpdateRemoveProductAPI.as_view(), name='update_remove_product'),
  path('product/additional-info/add/<int:pk>', api.AddProductAdditionalInfoAPI.as_view(), name='add_additional_info'),
]