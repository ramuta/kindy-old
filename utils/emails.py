from django.core.mail import send_mail, EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


def send_invite_email(inviter, invitee, childcare, password):
    if inviter and invitee and childcare and password:
        subject = 'I created an account for you at our childcare website'
        #message = 'Hi! I created an account for you at the %s website. Sign up at http://www.kindy.at with your email. Password is: %s. Please change it at the first login. Regards, %s.' % (childcare.name, password, inviter.get_full_name())
        #send_mail(subject=subject, message=message, from_email=inviter.email, recipient_list=[invitee.email,], fail_silently=False)

        plaintext = get_template('email/user_invited.txt')
        htmly = get_template('email/user_invited.html')

        context = Context({
            'inviter': inviter.get_full_name(),
            'childcare': childcare,
            'password': password
        })

        text_content = plaintext.render(context)
        html_content = htmly.render(context)

        email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=inviter.email, to=[invitee.email,])
        email.attach_alternative(content=html_content, mimetype='text/html')
        email.send()


def send_user_added_email(inviter, invitee, childcare, role):
    if inviter and invitee and childcare:
        subject = 'I added you to the %s dashboard' % childcare

        plaintext = get_template('email/user_added.txt')
        htmly = get_template('email/user_added.html')

        context = Context({
            'inviter': inviter.get_full_name(),
            'childcare': childcare,
            'role': role
        })

        text_content = plaintext.render(context)
        html_content = htmly.render(context)

        email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=inviter.email, to=[invitee.email, ])
        email.attach_alternative(content=html_content, mimetype='text/html')
        email.send()