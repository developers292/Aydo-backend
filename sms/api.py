from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import SmsVerificationCodeSerializer
from random import randrange
from .tasks import send_verification_code


class SmsVerificationCodeAPI(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):

        serializer = SmsVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_no = serializer.validated_data['phone_no']
        code = randrange(100000,999999)
        msg = f'کد فعال سازی حساب شما در آیدو : {code}'
        params = {
            'sender':'',
            'receptor': str(phone_no), #multiple mobile number, split by comma
            'message': msg,
        }

        # send verification code asynchronously with celery
        send_verification_code.delay(params)

        context = {
            'code':code
        }
        return Response(context)
