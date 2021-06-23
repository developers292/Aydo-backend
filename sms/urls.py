from django.urls import path, include
from . import api

urlpatterns = [
  path('verification-code', api.SmsVerificationCodeAPI.as_view(), name='verification_code'),
]