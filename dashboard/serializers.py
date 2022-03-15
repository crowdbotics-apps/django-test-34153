from rest_framework import serializers
from rest_framework.response import Response

from datetime import datetime

from datetime import datetime 

from .models import App


class AppSerializer(serializers.ModelSerializer):
    # Serializer used for GET Endpoint of App Model

    class Meta:
        model = App
        fields = ['id', 'name', 'description', 'type', 'framework', 'domain_name', 'screenshot', 'user', 'created_at', 'updated_at']


class PostAppSerializer(serializers.ModelSerializer):
    # Class should be renamed to be more descriptive of what it is used for
    # Serializer used for POST, PUT, and PATCH endpoints of App Model

    class Meta:
        model = App
        fields = ['name', 'description', 'type', 'framework', 'domain_name']

    def create(self, validated_data):
        """
            Create New App Entry, User assigned to request.user
            created_at populated automatically
        """
        app = App.objects.create(**validated_data)
        app.user = self.context['request'].user
        app.created_at = datetime.now()
        app.save()
        return app

    def update(self, instance, validated_data):
        
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.framework = validated_data.get('framework', instance.framework)
        instance.domain_name = validated_data.get('domain_name', instance.domain_name)
        instance.updated_at = datetime.now()
        print("TEST!!!!!")
        instance.save()

        return instance

    def partial_update(self, instance, validated_data):

        instance.update(**validated_data)
        instance.updated_at = datetime.now()
        print("PARTIAL TEST!!!!!")
        instance.save()

        return instance
