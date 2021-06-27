from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .permissions import IsManager
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from shop.models import Product, Category, AdditionalProductInfo, ProductImage, Comment
from django.http import Http404
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer
from shop.serializers import CommentReadSerializer
from Aydo.utils.pagination import CustomPagination
from .serializers import (CategoryWriteSerializer,
                          ProductWriteSerializer,
                          AdditionalProductInfoWriteSerializer,
                          ProductImageWriteSerializer,
                          UserEditSerializer,
                          CommentEditSerializer)



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



class AddProductAdditionalInfoAPI(APIView):
    """
    Add any key,value data to a 
    product as additional info
    """
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def get_object(self, pk):

        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise Http404
    

    def validate(self, data, related_product):
        
        for key,value in data.items():
            obj = {
                "key":key,
                "value":value,
                "product":related_product.id
            }
            serializer = AdditionalProductInfoWriteSerializer(data=obj)
            serializer.is_valid(raise_exception=True)


    def post(self, request, pk):
        
        product = self.get_object(pk)
        self.validate(data=request.data, related_product=product)
        for key,value in request.data.items():
            data = {
                "key":key,
                "value":value,
                "product":product.id
            }
            serializer = AdditionalProductInfoWriteSerializer(data=data)
            serializer.is_valid(raise_exception=False)
            serializer.save()
        
        return Response(status=status.HTTP_201_CREATED)
    


class UpdateRemoveProductAdditionalInfoAPI(APIView):
    """
    update or remove an additional info
    instance on a product
    """
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def get_object(self, pk):

        try:
            return AdditionalProductInfo.objects.get(id=pk)
        except AdditionalProductInfo.DoesNotExist:
            raise Http404
    

    def put(self, request, pk):

        obj = self.get_object(pk)
        serializer = AdditionalProductInfoWriteSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):

        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class AddProductImageAPI(APIView):
    """
    add an image to product's image gallery
    """
    permission_classes = [permissions.IsAuthenticated, IsManager]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_object(self, pk):

        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise Http404


    def post(self, request, pk):

        product = self.get_object(pk)
        serializer = ProductImageWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RemoveProductImageAPI(APIView):
    """
    remove an image from product gallery
    """
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def get_object(self, pk):

        try:
            return ProductImage.objects.get(id=pk)
        except ProductImage.DoesNotExist:
            raise Http404
    

    def delete(self, request, pk):

        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class UserListAPI(generics.ListAPIView):
  permission_classes = [permissions.IsAuthenticated, IsManager]
  serializer_class = UserSerializer
  
  def get_queryset(self):
      return get_user_model().objects.exclude(phone_no=self.request.user.phone_no)



class UserEditAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]


    def get_object(self, pk):

        try:
            return get_user_model().objects.get(id=pk)
        except get_user_model().DoesNotExist:
            raise Http404


    def put(self, request, pk):
        
        user = self.get_object(pk)
        serializer = UserEditSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CommentListAPI(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]
    serializer_class = CommentReadSerializer
    queryset = Comment.objects.all()
    pagination_class = CustomPagination




class CommentUserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]
    
    def get_object(self, pk):

        try:
            return get_user_model().objects.get(id=pk)
        except get_user_model().DoesNotExist:
            raise Http404
    

    def get(self, request, pk):

        user = self.get_object(pk)
        comments_serialized = CommentReadSerializer(user.product_comments.all(), many=True)
        return Response(comments_serialized.data)

    
    


            
class CommentEditAPI(APIView):
    """
    Edit comment attrs , for example change is_verified,
    active , or body of a comment
    """
    permission_classes = [permissions.IsAuthenticated, IsManager]


    def get_object(self, pk):

        try:
            return Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            raise Http404
    

    def put(self, request, pk):

        comment = self.get_object(pk)
        serializer = CommentEditSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

