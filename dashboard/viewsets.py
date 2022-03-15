from rest_framework import viewsets
from rest_framework.response import Response

from .models import App
from .serializers import AppSerializer, PostAppSerializer


# Create your views here.
class AppViewSet(viewsets.ModelViewSet):
    """
    AppViewSet
    """
    queryset = App.objects.all()
    serializer_class = AppSerializer


    def get_serializer_class(self):

        if self.request.method == 'GET':
            return AppSerializer

        elif self.request.method == 'POST':
            return PostAppSerializer

        elif self.request.method == 'PUT':
            return PostAppSerializer

        elif self.request.method == 'PATCH':
            return PostAppSerializer
