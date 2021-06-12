from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CartSerializer
from rest_framework import permissions
from .models import Cart
from rest_framework import status
from django.http import Http404




class ListCartAPI(APIView):
    """
    list cart content, or create a new cart item
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = Cart.objects.filter(owner=self.request.user)
        cart_serialized = CartSerializer(cart, many=True)
        return Response(cart_serialized.data)
    
    def post(self, request):

        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            owner = self.request.user
            if Cart.objects.filter(owner=owner, product=product).exists():
                context = {
                    'detail':'این محصول قبلا به کارت خرید اضافه شده است'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DetailCartAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    """
    update or delete an Cart instance
    """

    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404

    def put(self, request, pk):

        cart = self.get_object(pk)
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        cart = self.get_object(pk)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
