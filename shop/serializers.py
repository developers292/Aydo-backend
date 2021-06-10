from rest_framework import serializers
from .models import Product, AdditionalProductInfo, ProductImage


class AdditionalProductInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdditionalProductInfo
        fields = ('__all__')


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('__all__')


class ProductSerializer(serializers.ModelSerializer):
    additional_info = AdditionalProductInfoSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('__all__')