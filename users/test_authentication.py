from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import Task

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alexa', password='123')
        self.token = Token.objects.create(user=self.user)

    def test_user_login(self):
        url = reverse('token_obtain')  # Assuming 'login' is the name of the URL pattern for login
        response = self.client.post(url, {'username': 'alexa', 'password': '123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_token_generation(self):
        token = Token.objects.get(user=self.user)
        self.assertIsNotNone(token)
        self.assertEqual(token.user, self.user)

    def test_access_protected_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('task-list')  # Assuming 'task-list' is a protected endpoint
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_protected_endpoint_without_token(self):
        task = Task.objects.create(title="Test Task 1", description="Description 1", status=False)
        task = Task.objects.create(title="Test Task 2", description="Description 2", status=True)

        url = reverse('task-detail', args=[task.pk])  # Assuming 'task-list' is a protected endpoint
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)