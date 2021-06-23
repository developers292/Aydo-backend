from celery import task
from .kavenegar_sms_api import SmsAPI

@task
def send_verification_code(params):

    api = SmsAPI()
    api.send_sms(params)
    
