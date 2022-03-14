from rest_framework import serializers
from rest_framework.response import Response

from datetime import datetime

from .models import App


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name', 'description', 'type', 'framework', 'domain_name', 'screenshot', 'user', 'created_at', 'updated_at']


    def create(self, validated_data):
        """
        Test Things Here
        """
        app = App(name=validated_data.get('name'),
                  description=validated_data.get('description'),
                  type=validated_data.get('type'),
                  framework=validated_data.get('framework'),
                  domain_name=validated_data.get('domain_name'),
                  user=self.context['request'].user,
                  created_at = datetime.now())

        app.save()
        
        return app