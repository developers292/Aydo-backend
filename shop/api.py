from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import ProductSerializer, CategorySerializer, CommnetWriteSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Comment
from django.http import Http404
from django.db.models import Prefetch


class ListProductAPI(APIView):
    permission_classes = [permissions.AllowAny,]

    def get_category(self, category_id):

        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise Http404
    

    def get(self, request, category_id=None):

        category = None
        products = Product.objects.prefetch_related(Prefetch('comments',queryset=Comment.verified_and_active.all()))
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
        product_serialized = ProductSerializer(product)
        return Response(product_serialized.data)




class ListCategoryAPI(APIView):
    permission_classes = [permissions.AllowAny,]

    def get(self, request):
        
        categories = Category.objects.filter(parent=None)
        categories_serialized = CategorySerializer(categories, many=True)
        return Response(categories_serialized.data)


class DetailCategoryAPI(APIView):
    permission_classes = [permissions.AllowAny,]

    def get_object(self, pk):

        try:
            return Category.objects.get(id=pk)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):

        category = self.get_object(pk)
        category_serialized = CategorySerializer(category)
        return Response(category_serialized.data)



class AddCommentAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):

        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise Http404
    

    def post(self, request, pk):

        product = self.get_object(pk)
        serializer = CommnetWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                owner=self.request.user,
                product=product
            )
            return Response(status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



