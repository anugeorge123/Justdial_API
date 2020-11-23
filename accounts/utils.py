import pyotp
from random import randint
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

User = get_user_model()

def otp_generation():
    range_start = 10**(6-1)
    range_end = (10**6)-1
    return randint(range_start, range_end)


def password_reset_link_email(email, request):
    user= User.objects.filter(email=email).first()
    secret = pyotp.random_base32()
    otp = otp_generation()
    user.rp_otp = otp
    user.save()
    from_email = settings.EMAIL_HOST_USER
    to = email
    message = render_to_string('mail/password-reset-template.html', {
        'otp': otp,
        'reset_password_url': "http://127.0.0.1:8000/accounts/password-reset-confirm/?token="+str(otp).format(
            request.META['HTTP_HOST'], otp),
        'mobile':True,
        'use_https': request.is_secure(),
        'site': get_current_site(request)

    })
    msg = EmailMessage('Password Reset Email - Sample Project', message, from_email, [to])
    msg.content_subtype = "html"
    msg.send()


def confirmation_email(email, request):
    from_email = settings.EMAIL_HOST_USER
    to = email
    message =" This is a confirmation mail from sample project."
    msg = EmailMessage('Welcome Email - Sample Project', message, from_email, [to])
    msg.content_subtype = "html"
    print("dsds",msg)
    msg.send()



