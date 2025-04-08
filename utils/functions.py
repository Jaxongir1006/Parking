from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


def send_verification_email(email,token):
    
    sender = settings.EMAIL_HOST_USER
    subject = "Activate you email for IJASMIN"
    text = f"Verify your email click this link {settings.SITE_URL}{reverse('verify')}?token={token}"
    
    return send_mail(subject,message=text,from_email=sender,recipient_list=[email])
    
    
    






