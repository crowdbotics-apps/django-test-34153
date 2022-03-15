import json

from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model

from .viewsets import AppViewSet, SubscriptionViewSet
from .serializers import AppSerializer, PlanSerializer, SubscriptionSerializer
from .models import App, Plan, Subscription

# Create your tests here.
client = Client()
User = get_user_model()

class TestListAllApps(TestCase):
    """
    Test that GET /api/v1/apps/ returns list of all Apps
    """

    def setUp(self):
        App.objects.create(name="Test 1", type="Web", framework="Django", domain_name="test_1")
        App.objects.create(name="Test 2", type="Web", framework="Django", domain_name="test_2")
        App.objects.create(name="Test 3", type="Mobile", framework="React Native", domain_name="test_3")


    def test_get_all_apps(self):

        response = client.get('/api/v1/apps/')

        apps = App.objects.all()

        serializer = AppSerializer(apps, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestListSingleApp(TestCase):
    """
    Test that /api/v1/apps/{id} returns the correct app
    """

    def setUp(self):
        self.app1 = App.objects.create(name="Test 1", type="Web", framework="Django", domain_name="test_1")
        self.app2 = App.objects.create(name="Test 2", type="Web", framework="Django", domain_name="test_2")
        
    def test_valid_app_response(self):

        response = client.get(f'/api/v1/apps/{self.app1.id}/')
        app = App.objects.get(id = self.app1.id)
        serializer = AppSerializer(app)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_app_response(self):
        response = client.get(f'/api/v1/apps/27/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TestAddSingleApp(TestCase):
    """
    Test POST /api/v1/apps/ will create a valid entry
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser')
        self.view = AppViewSet.as_view({'post':'create'})

        self.valid_app_payload = {
            'name': "Valid App",
            'type': 'Web',
            'framework': 'Django',
            'domain_name': 'valid_app'
        }

        self.invalid_app_payload = {
            'name': "",
            'type': 'Web',
            'framework': 'Django',
            'domain_name': 'valid_app'
        }

    def test_valid_app_create(self):
        request = self.factory.post('/api/v1/apps/', self.valid_app_payload)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_app_create(self):
        request = self.factory.post('/api/v1/apps/', self.invalid_app_payload)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestUpdateApp(TestCase):
    """
    Test PUT /api/v1/app/{id}
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser')
        self.app = App.objects.create(name="Test App", type="Web", framework="Django", domain_name="test_app")
        self.view = AppViewSet.as_view({'put':'update'})
        self.valid_app_payload = {
            'name': 'Valid App',
            'description': "Valid App Description",
            'type': 'Web',
            'framework': 'Django',
            'domain_name': 'valid_app'
        }

        self.invalid_app_payload = {
            'name': "",
            'type': 'Web',
            'framework': 'Django',
            'domain_name': 'valid_app'
        }

    def test_valid_app_update(self):
        request = self.factory.put(f'/api/v1/apps/{self.app.id}/', self.valid_app_payload)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.app.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_app_update(self):
        request = self.factory.put(f'/api/v1/apps/{self.app.id}/', self.invalid_app_payload)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.app.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestPartialUpdateApp(TestCase):
    """
    Test PATCH /api/v1/app/{id}
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser')
        self.app = App.objects.create(name="Test App", type="Web", framework="Django", domain_name="test_app")
        self.view = AppViewSet.as_view({'patch':'partial_update'})
        self.valid_app_payload = {
            'name': 'Valid App' 
        }

        self.invalid_app_payload = {
            'name': ""
        }

    def test_valid_app_update(self):
        request = self.factory.patch(f'/api/v1/apps/{self.app.id}/', self.valid_app_payload)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.app.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_app_update(self):
        request = self.factory.patch(f'/api/v1/apps/{self.app.id}/', self.invalid_app_payload)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.app.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDeleteApp(TestCase):
    """
    Test DELETE /api/v1/app/{id}
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser')
        self.app = App.objects.create(name="Test App", type="Web", framework="Django", domain_name="test_app")
        self.view = AppViewSet.as_view({'delete':'destroy'})
        

    def test_app_delete(self):
        request = self.factory.delete(f'/api/v1/apps/{self.app.id}/')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.app.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestListAllPlans(TestCase):
    """
    Test that GET /api/v1/plans/ returns list of all Plans
    """

    def setUp(self):
        Plan.objects.create(name="Plan 1", description="Plan 1", price=0)
        Plan.objects.create(name="Plan 2", description="Plan 2", price=10)
        Plan.objects.create(name="Plan 3", description="Plan 3", price=25)        


    def test_get_all_plans(self):

        response = client.get('/api/v1/plans/')

        plans = Plan.objects.all()

        serializer = PlanSerializer(plans, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestListSinglePlan(TestCase):
    """
    Test that /api/v1/apps/{id} returns the correct app
    """

    def setUp(self):
        self.plan1 = Plan.objects.create(name="Plan 1", description="Plan 1", price=0)
        self.plan2 = Plan.objects.create(name="Plan 2", description="Plan 2", price=10)
        
    def test_valid_plan_response(self):

        response = client.get(f'/api/v1/plans/{self.plan1.id}/')
        plan = Plan.objects.get(id = self.plan1.id)
        serializer = PlanSerializer(plan)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_plan_response(self):
        response = client.get(f'/api/v1/plans/27/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestListAllSubscriptions(TestCase):
    """
    Test that GET /api/v1/subscriptions/ returns list of all Active Subscriptions
    """

    def setUp(self):
        Subscription.objects.create(plan=1, app=1, active=True)
        Subscription.objects.create(plan=2, app=2, active=True)
        Subscription.objects.create(plan=2, app=1, active=False)        


    def test_get_all_subscriptions(self):

        response = client.get('/api/v1/subscriptions/')

        subs = Subscription.objects.filter(active=True).all()

        serializer = SubscriptionSerializer(subs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestListSingleSubscription(TestCase):
    """
    Test that /api/v1/subscriptions/{id} returns the correct subscription
    """

    def setUp(self):
        self.sub1 = Subscription.objects.create(plan=1, app=1, active=True)
        self.sub2 = Subscription.objects.create(plan=2, app=2, active=True)
        
    def test_valid_subscription_response(self):

        response = client.get(f'/api/v1/subscriptions/{self.sub1.id}/')
        sub = Subscription.objects.filter(id=self.sub1.id).first()
        serializer = SubscriptionSerializer(sub)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_subscription_response(self):
        response = client.get(f'/api/v1/subscriptions/27/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestAddSingleSubscription(TestCase):
    """
    Test POST /api/v1/subscriptions/ will create a valid entry
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser')
        self.view = SubscriptionViewSet.as_view({'post':'create'})
        self.app = App.objects.create(name="Test App", type="Web", framework="Django", domain_name="test_app")

        self.valid_app_payload = {
            'plan': "1",
            'app': f'{self.app.id}',
            'active': 'true'
        }

        self.invalid_app_payload = {
            'plan': "",
            'app': f'{self.app.id}',
            'active': 'true'
        }

    def test_valid_subscription_create(self):
        request = self.factory.post('/api/v1/subscriptions/', self.valid_app_payload)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_subscription_create(self):
        request = self.factory.post('/api/v1/subscriptions/', self.invalid_app_payload)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUpdateSubscription(TestCase):
    """
    Test PUT /api/v1/subscriptions/{id}
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser')
        self.sub = Subscription.objects.create(plan=0, app=0, active=True)
        self.view = SubscriptionViewSet.as_view({'put':'update'})
        self.valid_app_payload = {
            'plan': '1',
            'app': "1",
            'active': 'true'
        }

        self.invalid_app_payload = {
            'plan': '',
            'app': "1",
            'active': 'true'
        }

    def test_valid_subscription_update(self):
        request = self.factory.put(f'/api/v1/subscriptions/{self.sub.id}/', self.valid_app_payload)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.sub.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_app_update(self):
        request = self.factory.put(f'/api/v1/subscriptions/{self.sub.id}/', self.invalid_app_payload)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.sub.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestPartialUpdateSubscription(TestCase):
    """
    Test PATCH /api/v1/subscription/{id}
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser')
        self.sub = Subscription.objects.create(plan=0, app=0, active=True)
        self.view = SubscriptionViewSet.as_view({'patch':'partial_update'})
        self.valid_app_payload = {
            'plan': '1' 
        }

        self.invalid_app_payload = {
            'plan': ""
        }

    def test_valid_subscription_update(self):
        request = self.factory.patch(f'/api/v1/subscriptions/{self.sub.id}/', self.valid_app_payload)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.sub.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_subscription_update(self):
        request = self.factory.patch(f'/api/v1/subscriptions/{self.sub.id}/', self.invalid_app_payload)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.sub.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)