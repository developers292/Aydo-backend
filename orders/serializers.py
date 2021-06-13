from rest_framework import serializers
from .models import Province, City, Order


class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Province
        fields = ('__all__')


class CitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()

    class Meta:
        model = City
        fields = ('__all__')



class OrderCreateSerializer(serializers.ModelSerializer):
    province = serializers

    class Meta:
        model = Order
        fields = (
            'province', 'city', 'street',
            'alley', 'postal_code', 'detail_address',
            'delivery_date', 'online_payment'
        )
        extra_kwargs = {
            'province': {'allow_null': False, 'required': True},
            'city': {'allow_null': False, 'required': True}
        }
    
    def create(self, validated_data):
        """
        just overrided create() in order to 
        return an instance after creating
        """
        return Order.objects.create(**validated_data)
    