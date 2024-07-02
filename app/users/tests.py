# Create your tests here.

# class SignUpTest(TestCase):
#     def test_sign_up_page_exists(self):
#         response = self.client.get(reverse('profile'))
#         print(response['location'])
#         self.assertEqual(response.status_code, 200)


# from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import Client
import unittest
from django.urls import reverse


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        try:
            self.user = User.objects.create_user(
                "john3", "john3@email.com", "bareco3t@wer"
            )
        except:
            print("it already exist")

    def testProfileView(self):
        self.client.login(username="john3", password="bareco3t@wer")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
