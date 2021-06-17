from rest_framework import serializers
from shop.models import Category



class CreateCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('__all__')
        read_only_fields = ('id',)