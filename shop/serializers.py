from rest_framework import serializers
from .models import (Product, AdditionalProductInfo,
                     ProductImage, Category, Comment)

from accounts.serializers import UserSerializer

class AdditionalProductInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdditionalProductInfo
        fields = ('__all__')


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('__all__')


class CommentReadSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Comment
        fields = ('__all__')


class CommnetWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('body',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'parent', 'name', 'slug', 'children')
    
    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['children'] = CategorySerializer(many=True)
        return fields



class ProductSerializer(serializers.ModelSerializer):
    additional_info = AdditionalProductInfoSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    comments = CommentReadSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('__all__')



