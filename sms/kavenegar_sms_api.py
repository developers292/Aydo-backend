from kavenegar import *
from django.conf import settings


class SmsAPI(object):

    def __init__(self):

        self.api_key = settings.KAVENEGAR['API_KEY']
    

    def send_sms(self, params):

        try:
            api = KavenegarAPI(apikey=self.api_key)
            response = api.sms_send(params)
            return response
        except APIException as e: 
            print(e)
        except HTTPException as e:
            print(e)



