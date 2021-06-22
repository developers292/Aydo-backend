from django.contrib import admin
from .models import (Category, Product,
                     AdditionalProductInfo, ProductImage,
                     Comment)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}


class AdditionalProductInfoInline(admin.TabularInline):
    model = AdditionalProductInfo

class ProductImageInline(admin.StackedInline):
    model = ProductImage

class CommentInline(admin.StackedInline):
    model = Comment

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [AdditionalProductInfoInline, ProductImageInline, CommentInline]


@admin.register(AdditionalProductInfo)
class AdditionalProductInfoAdmin(admin.ModelAdmin):
    list_display = ['product', 'key', 'value']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'owner', 'is_verified', 'active']
    list_display_links = ['product', 'owner']