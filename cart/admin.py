from django.contrib import admin
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'product', 'owner', 'quantity'
    ]
    list_filter = [
        'owner', 'product'
    ]
    raw_id_fields = ('product', 'owner')
