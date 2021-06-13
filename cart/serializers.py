from rest_framework import serializers
from .models import Cart
from shop.serializers import ProductSerializer
from shop.models import Product



class CartReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ('__all__')
    



class CartWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        exclude = ('owner',)
        read_only_fields = ('id',)
    
    def update(self, instance, validated_data):
        """ 
        override update() in order to being able 
        to update quantity only , not product field
        """
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance


    

    
