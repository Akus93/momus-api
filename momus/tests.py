from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from momus.models import UserProfile


class BaseApiTest(APITestCase):

    def setUp(self):
        user = User.objects.create_user(username='user', email='user@test.com', password='user123password',
                                        first_name='John', last_name='Snow')
        self.test_user = UserProfile.objects.get(user=user)
        self.test_user_token = Token.objects.create(user=user, key='RANDOMuserTOKEN')
        self.USERS_REGISTERED = 1


class RegistrationTests(BaseApiTest):

    def test_success_registration(self):
        url = '/auth/registration/'
        data = {'email': 'dawid.rdzanek@protonmail.com', 'password1': 'testpassword123', 'password2': 'testpassword123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), self.USERS_REGISTERED + 1)
        self.assertEqual(UserProfile.objects.count(), self.USERS_REGISTERED + 1)
        self.assertEqual(UserProfile.objects.last().user.username, 'dawid.rdzanek')
        self.assertEqual(UserProfile.objects.last().user.email, 'dawid.rdzanek@protonmail.com')
        self.assertEqual(Token.objects.filter(user__username='dawid.rdzanek').count(), 1)
        self.assertEqual(response.data, {'key': Token.objects.get(user__username='dawid.rdzanek').key})

    def test_success_registration_add_number_if_username_exist(self):
        url = '/auth/registration/'
        data = {'email': 'user@otherdomain.com', 'password1': 'testpassword123', 'password2': 'testpassword123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), self.USERS_REGISTERED + 1)
        self.assertEqual(UserProfile.objects.count(), self.USERS_REGISTERED + 1)
        self.assertTrue(User.objects.get(email='user@otherdomain.com').username.startswith('user'))

    def test_unsuccess_registration_email_exist(self):
        url = '/auth/registration/'
        data = {'email': 'user@test.com', 'password1': 'testpassword123', 'password2': 'testpassword123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), self.USERS_REGISTERED)
        self.assertEqual(UserProfile.objects.count(), self.USERS_REGISTERED)
        self.assertTrue('email' in response.data)

    def test_unsuccess_registration_different_passwords(self):
        url = '/auth/registration/'
        data = {'email': 'other.test@student.com', 'password1': 'testpassword123', 'password2': 'differentpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), self.USERS_REGISTERED)
        self.assertEqual(UserProfile.objects.count(), self.USERS_REGISTERED)

    def test_unsuccess_registration_wrong_email_format(self):
        url = '/auth/registration/'
        data = {'email': 'teststudent.c', 'password1': 'testpassword123', 'password2': 'testpassword123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), self.USERS_REGISTERED)
        self.assertEqual(UserProfile.objects.count(), self.USERS_REGISTERED)
        self.assertTrue('email' in response.data)


class LoginTests(BaseApiTest):

    def test_success_login(self):
        url = '/auth/login/'
        data = {'email': 'user@test.com', 'password': 'user123password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'key': Token.objects.get(user__username='user').key})

    def test_unsuccess_login_wrong_credentials(self):
        url = '/auth/login/'
        data = {'email': 'wrong@test.com', 'password': 'wrongpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
