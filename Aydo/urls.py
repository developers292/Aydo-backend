from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/cart', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/payment/', include('payment.urls')),
    path('api/manager/', include('manager.urls')),
    path('api/sms/', include('sms.urls')),
    path('api/shop/', include('shop.urls')),
]

urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
