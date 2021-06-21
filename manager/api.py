from rest_framework.views import APIView
from .serializers import CategoryWriteSerializer, ProductWriteSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .permissions import IsManager
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from shop.models import Product, Category
from django.http import Http404



class CreateCategoryAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def post(self, request):

        serializer = CategoryWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateRemoveCategoryAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def get_object(self, pk):

        try:
            return Category.objects.get(id=pk)
        except Category.DoesNotExist:
            raise Http404
    
    
    def put(self, request, pk):

        category = self.get_object(pk)
        serializer = CategoryWriteSerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request, pk):

        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class CreateProductAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def post(self, request):
    
        serializer = ProductWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UpdateRemoveProductAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_object(self, pk):

        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise Http404


    def put(self, request, pk):

        product = self.get_object(pk)
        serializer = ProductWriteSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):

        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)