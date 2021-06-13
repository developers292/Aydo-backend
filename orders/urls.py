from django.urls import path, include
from . import api

urlpatterns = [
  path('province', api.ListProvinceAPI.as_view(), name='province_list'),
  path('city', api.ListCityAPI.as_view(), name='city_list'),
]