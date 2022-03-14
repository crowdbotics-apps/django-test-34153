from rest_framework import serializers

from .models import App


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name', 'description', 'type', 'framework', 'domain_name', 'screenshot', 'user', 'created_at', 'updated_at']