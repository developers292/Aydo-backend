from rest_framework.views import APIView
from rest_framework import permissions
from zeep import Client, Transport
from django.shortcuts import redirect
from django.http import Http404
from .Gateways import zarinpal
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from .models import ZarinpalPaymentInfo


class ZarinpalSendRequest(APIView):
    permission_classes= [permissions.IsAuthenticated,]

    def get(self, request):

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            if order:
                amount = sum(item.get_cost() for item in order.items.all())
                mobile = order.user.phone_no
                email = order.user.email
                zarinpal_gateway = zarinpal.Zarinpal()
                response = zarinpal_gateway.payment_request(
                    amount=amount,
                    mobile=mobile,
                    email=email
                )

                if not response:
                    context = {
                        'status':'error',
                        'detail':'در حال حاضر درگاه بانکی پاسخ گو نیست',
                        'ref_code':order.ref_code
                    }
                    return Response(context)

                if response.Status == 100:
                    context = {
                        'status':'ok',
                        'url':'https://banktest.ir/gateway/zarinpal/pg/StartPay/'+str(response.Authority),
                        'amount':amount,
                        'ref_code':order.ref_code
                    }
                    return Response(context)
                elif response.Status == -1:
                    context = {
                        'status':'error',
                        'detail':'اطلاعات ارسال شده ناقص است',
                        'ref_code':order.ref_code
                    }
                    return Response(context)
                elif response.Status == -2:
                    context = {
                        'status':'error',
                        'detail':'اتصال به درگاه انجام نشد',
                        'ref_code':order.ref_code
                    }
                    return Response(context)
                elif response.Status == -3:
                    context = {
                        'status':'error',
                        'detail':'با توجه به محدودیت های شاپرک امکان پرداخت با رقم درخواست شده میسر نمیباشد',
                        'ref_code':order.ref_code
                    }
                    return Response(context)
                elif response.Status == -22:
                    context = {
                        'status':'error',
                        'detail':'تراکنش ناموفق',
                        'ref_code':order.ref_code
                    }
                    return Response(context)
                else:
                    context = {
                        'status':'error',
                        'detail':f'خطای {str(response.Status)}',
                        'ref_code':order.ref_code
                    }
                    return Response(context)

            else:
                raise Http404
        
        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ZarinpalVerify(APIView):
    permission_classes= [permissions.IsAuthenticated,]

    def get(self, request):

        if request.GET.get('Status') == 'OK':

            order_id = request.GET['order_id']
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()
            obj = ZarinpalPaymentInfo(order=order, Authority=request.GET['Authority'])
            obj.save()

            zarinpal_gateway = zarinpal.Zarinpal()
            response = zarinpal_gateway.payment_verification(
                Authority=request.GET['Authority'],
                amount=request.GET['amount']
            )

            if not response:
                context = {
                    'status':'error',
                    'detail':'درگاه به درخواست تایید پرداخت پاسخگو نیست',
                    'ref_code':order.ref_code
                }
                return Response(context)

            if response.Status == 100:
                for item in order.items.all():
                    related_product = item.product
                    related_product.quantity = related_product.quantity - 1
                    if related_product.quantity < 1:
                        related_product.available = False
                    related_product.save()
                
                order.payment_verified = True
                order.save()

                obj.RefID = str(response.RefID)
                obj.status_code = response.Status
                obj.save()

                context = {
                    'status':'ok',
                    'RefID':str(response.RefID),
                    'ref_code':order.ref_code
                }
                return Response(context)
            
            elif response.Status == 101:
                context = {
                    'status':'ok',
                    'detail':'عملیات پرداخت قبلا با موفقیت ثبت شده است',
                    'ref_code':order.ref_code
                }
                return Response(context)
    
            elif response.Status == -1:
                obj.status_code = response.Status
                obj.save()
                context = {
                    'status':'error',
                    'detail':'اطلاعات ارسال شده ناقص است',
                    'ref_code':order.ref_code
                }
                return Response(context)
            elif response.Status == -2:
                obj.status_code = response.Status
                obj.save()
                context = {
                    'status':'error',
                    'detail':'اتصال به درگاه انجام نشد',
                    'ref_code':order.ref_code
                }
                return Response(context)
            elif response.Status == -3:
                obj.status_code = response.Status
                obj.save()
                context = {
                    'status':'error',
                    'detail':'با توجه به محدودیت های شاپرک امکان پرداخت با رقم درخواست شده میسر نمیباشد',
                    'ref_code':order.ref_code
                }
                return Response(context)
            elif response.Status == -22:
                obj.status_code = response.Status
                obj.save()
                context = {
                    'status':'error',
                    'detail':'تراکنش ناموفق',
                    'ref_code':order.ref_code
                }
                return Response(context)
            elif response.Status == -33:
                obj.status_code = response.Status
                obj.save()
                context = {
                    'status':'error',
                    'detail':'رقم تراکنش با رقم پرداخت شده مطابقت ندارد',
                    'ref_code':order.ref_code
                }
                return Response(context)
            else:
                obj.status_code = response.Status
                obj.save()
                context = {
                    'status':'error',
                    'detail':f'خطای {str(response.Status)}',
                    'ref_code':order.ref_code
                }
                return Response(context)

        else:
            order_id = request.GET['order_id']
            order = Order.objects.get(id=order_id)
            context = {
                'status':'error',
                'detail':'تراکنش  ناموقق ',
                'ref_code':order.ref_code

            }
            return Response(context)
