from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from django.http import Http404


class ListProductAPI(APIView):
    permission_classes = [permissions.AllowAny,]

    def get_category(self, category_id):

        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise Http404
    

    def get(self, request, category_id=None):

        category = None
        products = Product.objects.all()
        if category_id:
            category = self.get_category(category_id)
            products = products.filter(category=category)

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




class ListCategoryAPI(APIView):
    permission_classes = [permissions.AllowAny,]

    def get(self, request):
        
        categories = Category.objects.filter(parent=None)
        categories_serialized = CategorySerializer(categories, many=True)
        return Response(categories_serialized.data)

