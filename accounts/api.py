from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle
from .serializers import (UserSerializer, RegisterSerializer,
                          LoginSerializer, ChangePasswordSerializer,
                          ResetPasswordSerializer)

# Register API
class RegisterAPI(generics.GenericAPIView):
  serializer_class = RegisterSerializer
  permission_classes = [permissions.AllowAny,]

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
  permission_classes = [permissions.AllowAny,]
  serializer_class = LoginSerializer
  throttle_scope = 'login'
  throttle_classes = [ScopedRateThrottle,]
  
  
  def post(self, request, *args, **kwargs):

    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data

    if AuthToken.objects.filter(user=user).count() > 5: # let 5 as maximum number of user's acive sessions
      AuthToken.objects.filter(user=user).delete() 

    _, token = AuthToken.objects.create(user)
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": token
    })


# Get User API
class UserDetailAPI(generics.RetrieveUpdateAPIView):
  permission_classes = [permissions.IsAuthenticated,]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user
  
  def get_serializer(self, *args, **kwargs):
    kwargs['partial'] = True
    return super(UserDetailAPI, self).get_serializer(*args, **kwargs)



class ChangePasswordAPI(generics.GenericAPIView):
  permission_classes = [permissions.IsAuthenticated,]
  serializer_class = ChangePasswordSerializer
  throttle_scope = 'change_password'
  throttle_classes = [ScopedRateThrottle,]
  
  def get_object(self):
    return self.request.user
  
  def put(self, request, *args, **kwargs):

    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    return Response(status=status.HTTP_200_OK)



class ResetPasswordAPI(APIView):
  permission_classes = [permissions.AllowAny,]
  throttle_scope = 'reset_password'
  throttle_classes = [ScopedRateThrottle,]

  def post(self, request):

    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=status.HTTP_200_OK)


