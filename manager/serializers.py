from rest_framework import serializers
from shop.models import Category, Product, AdditionalProductInfo, ProductImage, Comment
from django.contrib.auth import get_user_model



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


class AdditionalProductInfoWriteSerializer(serializers.ModelSerializer):
    """ serializer for add, update and remove additional info to a product """

    class Meta:
        model = AdditionalProductInfo
        fields = ('__all__')
        read_only_fields = ('id',)
        extra_kwargs = {
            'key':{
                'error_messages':{
                    'required':'فیلد کلید باید ارسال شود',
                    'blank':'مقدار کلید نمیتواند خالی باشد'
                }
            },
            'value':{
                'error_messages':{
                    'required':'فیلد مقدار باید ارسال شود',
                    'blank':'مقدار متناظر با یک کلید نمیتواند خالی باشد'
                }
            }
        }
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('product', 'key'),
                message="ثبت کلید تکراری برای محصول مجاز نیست"
            )
        ]


class ProductImageWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('__all__')
        read_only_fields = ('id','product')



class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'phone_no', 'email',
            'first_name', 'last_name',
            'has_permission_to_view_prices',
            'is_active'
        )
        read_only_fields = ('id',)


class CommentEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('__all__')
        read_only_fields = ('id',)