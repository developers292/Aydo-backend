from rest_framework import serializers
from shop.models import Category, Product



class CategoryWriteSerializer(serializers.ModelSerializer):
    """ serializer for create, update and delete category """

    class Meta:
        model = Category
        fields = ('__all__')
        read_only_fields = ('id',)



class ProductWriteSerializer(serializers.ModelSerializer):
    """ serializer for create, update and delete product """

    class Meta:
        model = Product
        exclude = ('created', 'updated')
        read_only_fields = ('id',)