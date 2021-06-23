from rest_framework import serializers


class SmsVerificationCodeSerializer(serializers.Serializer):
    phone_no = serializers.CharField()