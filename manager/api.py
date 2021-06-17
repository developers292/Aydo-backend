from rest_framework.views import APIView
from .serializers import CreateCategorySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .permissions import IsManager


class CreateCategoryAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def post(self, request):

        serializer = CreateCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)