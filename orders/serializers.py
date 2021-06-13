from rest_framework import serializers
from .models import Province, City


class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Province
        fields = ('__all__')


class CitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()

    class Meta:
        model = City
        fields = ('__all__')