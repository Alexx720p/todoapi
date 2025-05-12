from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters, response
from .serializer import TaskSerializer
from .models import Task


class CustomAnonRateThrottle(AnonRateThrottle):
    rate = '60/hour'

class TaskPagination(PageNumberPagination):
    page_size = 10

class TaskView(viewsets.ModelViewSet):
    throttle_classes = [CustomAnonRateThrottle]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return response({'message': 'This is a protected view'})

    queryset = Task.objects.all().order_by('id')
    serializer_class = TaskSerializer
    pagination_class = TaskPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'status']