from rest_framework import viewsets
from rest_framework.response import Response

from .models import App
from .serializers import AppSerializer

import logging

logger = logging.getLogger(__name__)
# Create your views here.
class AppViewSet(viewsets.ModelViewSet):
    """
    AppViewSet
    """
    queryset = App.objects.all()
    serializer_class = AppSerializer

    """
    def apps_list(self, request, *args, **kwargs):
        app_list = self.get_object()

        return Response(app_list)"""
