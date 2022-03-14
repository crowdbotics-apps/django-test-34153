from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class App(models.Model):

    APP_TYPE = [
        ('Web', 'Web'),
        ('Mobile', 'Mobile')
    ]

    APP_FRAMEWORK = [
        ('Django', 'Django'),
        ('React Native', 'React Native')
    ]

    name = models.CharField('Name', max_length=50)
    description = models.TextField('description', blank=True)
    type = models.CharField('Type', max_length=16, choices=APP_TYPE)
    framework = models.CharField('Framework', max_length=16, choices=APP_FRAMEWORK)
    domain_name = models.CharField('Domain Name', max_length=50)
    screenshot = models.URLField('Screenshot', max_length=200, blank=True)
    # subscription = models.ForeignKey(Subscription, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField('Created at', null=True)
    updated_at = models.DateTimeField('Updated at', null=True)


class Plan(models.Model):
    name = models.CharField('Name', max_length=20)
    description = models.TextField('Description', blank=False)
    price = models.DecimalField('Price', decimal_places=2, max_digits=5)
    created_at = models.DateTimeField('Created at', null=True)
    updated_at = models.DateTimeField('Updated at', null=True)


class Subscription(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    plan = models.ForeignKey(Plan, null=True, on_delete=models.SET_NULL)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    active = models.BooleanField('Active')
    created_at = models.DateTimeField('Created at', null=True)
    updated_at = models.DateTimeField('Updated at', null=True)