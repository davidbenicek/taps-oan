from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser, User
from taps_oan import views, urls
from .views import index

import unittest

class PageAccessTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test2', email='test@test2.com', password='passpass')
        self.factory = RequestFactory()

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_user(self):
        response = self.client.post("/taps_oan/register/", {
            "username": "testy",
            "email": "email@email.com", 
            "password": "password", 
            "password-confirm": "password" })
        user = User.objects.get(username="testy")
        self.assertEqual(user.email, "email@email.com")
        self.assertEqual(response.status_code, 200)