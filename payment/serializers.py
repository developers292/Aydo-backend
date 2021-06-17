from rest_framework import serializers
from orders.models import Order


class OrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    ref_code = serializers.CharField()

    def save(self):
        try:
            return Order.objects.get(
                id=self.validated_data['order_id'],
                ref_code=self.validated_data['ref_code']
            )
        except Order.DoesNotExist:
            return None
        