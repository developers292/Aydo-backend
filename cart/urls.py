from django.urls import path
from . import api

urlpatterns = [
  path('', api.ListCartAPI.as_view(), name='list_cart'),
  path('/<int:pk>', api.DetailCartAPI.as_view(), name='detail_cart'),
]