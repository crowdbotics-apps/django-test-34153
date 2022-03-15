from rest_framework import serializers, status
from rest_framework.response import Response

from datetime import datetime

from datetime import datetime 

from .models import App, Plan, Subscription


class AppSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = App
        fields = ['id', 
                  'name', 
                  'description', 
                  'type', 
                  'framework', 
                  'domain_name', 
                  'screenshot',
                  'subscription', 
                  'user', 
                  'created_at', 
                  'updated_at'
            ]
        read_only_fields = ('id', 
                            'screenshot', 
                            'subscription', 
                            'user', 
                            'created_at', 
                            'updated_at'
            )


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

        instance.save()

        return instance

    def partial_update(self, instance, validated_data):

        instance.update(**validated_data)
        instance.updated_at = datetime.now()
        
        instance.save()

        return instance


class PlanSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Plan
        fields = ['id', 
                  'name', 
                  'description', 
                  'price', 
                  'created_at', 
                  'updated_at'
        ]
        read_only_fields = ('id', 
                            'created_at', 
                            'updated_at'
            )


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ['id',
                  'user',
                  'plan',
                  'app',
                  'active',
                  'created_at',
                  'updated_at'
            ]
        read_only_fields = ('id',
                            'user',
                            'created_at',
                            'updated_at'
            )

    def create(self, validated_data):
        """
        Create New Subscription 
        """
        # Check for Valid Plan
        plan_id = validated_data['plan']
        
        # Need to validated it is a valid plan id

        # Check for Valid App
        app_id = validated_data['app']
        app = App.objects.filter(id=app_id).first()
        
        # Need to validated it is a valid app id

        # Set old Subscription to Inactive
        old_subs = Subscription.objects.filter(app=app_id, active=True).all()
        for sub in old_subs:
            sub.active = False
            sub.updated_at = datetime.now()
            sub.save()

        # Create Subscription
        new_sub = Subscription.objects.create(**validated_data)
        new_sub.user = self.context['request'].user
        new_sub.active = True # Not sure why this wasnt working from validated_data
        new_sub.created_at = datetime.now()
        new_sub.save()

        # Update App to current Subscription ID
        app.subscription = new_sub.id
        app.updated_at = datetime.now()
        app.save()

        return new_sub

    def update(self, instance, validated_data):
        
        instance.plan = validated_data.get('plan', instance.plan)
        instance.app = validated_data.get('app', instance.app)
        instance.active = validated_data.get('active', instance.active)
        instance.updated_at = datetime.now()

        instance.save()

        return instance

    def partial_update(self, instance, validated_data):

        instance.update(**validated_data)
        instance.updated_at = datetime.now()
        
        instance.save()

        return instance