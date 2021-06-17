from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Province ,City, OrderItem
from cart.models import Cart
from rest_framework import status
from django.utils.crypto import get_random_string
from .serializers import (ProvinceSerializer,
                          CitySerializer,
                          OrderCreateSerializer)
    


class ListProvinceAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        provinces = Province.objects.all()
        provinces_serialized = ProvinceSerializer(provinces, many=True)
        return Response(provinces_serialized.data)


class ListCityAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        cities = City.objects.all()
        cities_serialized = CitySerializer(cities, many=True)
        return Response(cities_serialized.data)



class OrderCreateAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        
        cart_items = Cart.objects.filter(owner=self.request.user)
        if len(cart_items) < 1:
            context = {
                'detail':'کارت خرید شما خالی است'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(
                user=self.request.user
            )

            ref_code = str(order.id) + (get_random_string(length=4))
            order.ref_code = ref_code
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )

            # clear cart
            cart_items.delete()
            
            context = {
                'ref_code':order.ref_code,
                'order_id':order.id,
                'online_payment':order.online_payment
            }
            return Response(context, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




