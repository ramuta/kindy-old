from django.core.mail import send_mail


def send_invite_email(inviter, invitee, childcare, password):
    if inviter and invitee and childcare and password:
        subject = 'I created an account for you at our childcare website'
        message = 'Hi! I created an account for you at the %s website. Sign up at http://www.kindy.at with your email. Password is: %s. Please change it at the first login. Regards, %s.' % (childcare.name, password, inviter)
        send_mail(subject=subject, message=message, from_email=inviter.email, recipient_list=[invitee.email,], fail_silently=False)