from zeep import Client
from django.conf import settings


class Zarinpal(object):

    def __init__(self):

        self.client = Client(settings.ZARINPAL['wsdl'])
        self.CallbackURL = settings.ZARINPAL['CallbackURL']
        self.MERCHANT = settings.ZARINPAL['MERCHANT']


    def payment_request(self, amount, description='', email='', mobile=''):
        
        try:
            response = self.client.service.PaymentRequest(self.MERCHANT, amount, description, email, mobile, self.CallbackURL)
            return response
        except Exception:
            # perform a second try
            try:
                response = self.client.service.PaymentRequest(self.MERCHANT, amount, description, email, mobile, self.CallbackURL)
                return response
            except Exception:
                return None

    
    def payment_verification(self, Authority, amount):
        
        try:
            response = self.client.service.PaymentVerification(self.MERCHANT, Authority, amount)
            return response
        except Exception:
            # perform a second try
            try:
                response = self.client.service.PaymentVerification(self.MERCHANT, Authority, amount)
                return response
            except Exception:
                return None

            
