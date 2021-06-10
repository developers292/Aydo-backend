from django.contrib import admin
from .models import Category, Product, AdditionalProductInfo, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}


class AdditionalProductInfoInline(admin.TabularInline):
    model = AdditionalProductInfo

class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [AdditionalProductInfoInline, ProductImageInline]


@admin.register(AdditionalProductInfo)
class AdditionalProductInfoAdmin(admin.ModelAdmin):
    list_display = ['product', 'key', 'value']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')