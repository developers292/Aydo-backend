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
      'has_permission_to_view_prices',
      'is_active'
    )
    read_only_fields = (
      'id', 'has_permission_to_view_prices',
      'phone_no', 'is_active'
    )
  
  
  def update(self, instance, validated_data):
    """ Update a user and return it"""
    user = super().update(instance, validated_data)
    return user


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=4)
    phone_no = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):

      user = authenticate(
        phone_no=data['phone_no'],
        password=data['password']
      )
      if user:
        if user.is_active:
          user.set_password(data['new_password'])
          user.save()
          return user
        else:
          raise serializers.ValidationError("حساب شما موقتا غیر فعال شده است")

      raise serializers.ValidationError("شماره تماس یا رمز عبور نادرست است")



class ResetPasswordSerializer(serializers.Serializer):
  password = serializers.CharField(write_only=True, min_length=4)
  phone_no = serializers.CharField(write_only=True)

  def validate(self, data):

    try:
      user = get_user_model().objects.get(phone_no=data['phone_no'])
      return data
    except get_user_model().DoesNotExist:
      raise serializers.ValidationError('شماره تلفن نامعبتر است')
  
  def save(self):
    """ set new password """
    password = self.validated_data.pop('password')
    user = get_user_model().objects.get(phone_no=self.validated_data.pop('phone_no'))
    if password:
      user.set_password(password)
      user.save()



# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ('id', 'phone_no', 'password')
    extra_kwargs = {'password': {'write_only': True, 'min_length':4}}

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