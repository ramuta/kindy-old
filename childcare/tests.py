"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from model_mommy import mommy
from django.test import TestCase
from childcare.models import Childcare


class ChildcareViewsTestCase(TestCase):
    def _log_in(self):
        user = User.objects.create_user('test', 'test@test.si', 'test')
        user.save()
        if self.client.login(username='test', password='test'):
            return user
        return None

    def test_classroom_create(self):
        user = self._log_in()
        childcare = mommy.make(Childcare, slug='jana', pk=1)
        response = self.client.get(reverse('childcare_create'))
        self.assertEqual(response.status_code, 200)