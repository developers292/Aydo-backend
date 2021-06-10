from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

# User Serializer
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = (
      'id', 'phone_no', 'email',
      'first_name', 'last_name',
      'has_permission_to_view_prices'
    )


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ('id', 'phone_no', 'password')
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    user = get_user_model().objects.create_user(validated_data['phone_no'],validated_data['password'])

    return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
  phone_no = serializers.CharField()
  password = serializers.CharField()

  def validate(self, data):
    user = authenticate(**data)
    if user:
      if user.is_active:
        return user
      else:
        raise serializers.ValidationError("حساب شما موقتا غیر فعال شده است")

    raise serializers.ValidationError("شماره تماس یا رمز عبور نادرست است")