from django.contrib import admin
from .models import Province, City, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'postal_code', 'province', 'city',
                    'paid', 'recieved', 'refund_requested', 'refund_granted',
                    'created', 'updated', 'online_payment']
                    
    list_filter = ['paid', 'created', 'updated', 'refund_requested', 'refund_granted']
    inlines = [OrderItemInline]


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(City)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'province']
    