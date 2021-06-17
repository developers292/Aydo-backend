from django.urls import path, include
from . import api

urlpatterns = [
  path('zarinpal', api.ZarinpalSendRequest.as_view(), name='zarinpal_payment_request'),
  path('zarinpal-verify', api.ZarinpalVerify.as_view(), name='zarinpal_payment_verify'),
]