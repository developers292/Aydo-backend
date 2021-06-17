from django.urls import path
from . import api

urlpatterns = [
  path('create-category', api.CreateCategoryAPI.as_view(), name='create_category'),
]