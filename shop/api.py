from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from django.http import Http404


class ListProductAPI(APIView):
    permission_classes = [permissions.AllowAny,]
    
    def get(self, request):
        products = Product.objects.all()
        products_serialized = ProductSerializer(products, many=True)
        return Response(products_serialized.data)


class DetailProductAPI(APIView):
    permission_classes = [permissions.AllowAny,]

    def get_object(self, pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        product_serializer = ProductSerializer(product)
        return Response(product_serializer.data)


        
