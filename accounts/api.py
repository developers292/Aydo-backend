from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.views import APIView

# Register API
class RegisterAPI(generics.GenericAPIView):
  serializer_class = RegisterSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    context = {
      'user':UserSerializer(user, context=self.get_serializer_context()).data
    }
    return Response(context)

# Login API
class LoginAPI(generics.GenericAPIView):
  serializer_class = LoginSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    _, token = AuthToken.objects.create(user)
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": token
    })

# Get User API
class UserAPI(generics.RetrieveAPIView):
  permission_classes = [
    permissions.IsAuthenticated,
  ]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user



class GetSessionKey(APIView):
  permission_classes = [
    permissions.IsAuthenticated,
  ]

  def get(self, request, *args, **kwargs):
    #request.session['cart'] = {'id':'2'}
    #request.session.modified = True
    
    context = {
      'cart':request.session['cart']
    }
    """
    context = {
      'stat':'ok'
    }
    """
    return Response(context, status=200)

