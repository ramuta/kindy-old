from django.db import models
from userena.models import UserenaBaseProfile
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


GENDER_CHOICES = (
    ('M', 'male'),
    ('F', 'female'),
)


class KindyUser(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='kindy_user')
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    address = models.CharField(max_length=255, blank=True)
    current_town = models.CharField(max_length=255, blank=True)
    current_country = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)