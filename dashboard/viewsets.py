from rest_framework import viewsets
from rest_framework.response import Response

from .models import App, Plan, Subscription
from .serializers import (
    AppSerializer, 
    PlanSerializer,
    SubscriptionSerializer
)


# Create your views here.
class AppViewSet(viewsets.ModelViewSet):
    """
    AppViewSet
    """
    queryset = App.objects.all()
    serializer_class = AppSerializer
    


class PlanViewSet(viewsets.ModelViewSet):
    """
    PlanViewSet
    """
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    http_method_names = ['get']


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    SubscriptionViewSet
    """
    queryset = Subscription.objects.filter(active=True).all()
    serializer_class = SubscriptionSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
