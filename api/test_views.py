from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Task
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class TaskViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alexa', password='123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION= 'Token ' + self.token.key)
        
        Task.objects.create(title="Test Task 1", description="Description 1", status=False)
        Task.objects.create(title="Test Task 2", description="Description 2", status=True)

    def test_get_tasks(self):
        url = reverse('task-list') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_search_tasks(self):
        task = Task.objects.get(title='Test Task 1')
        url = reverse('task-detail', args=[task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)