from rest_framework import serializers
from django.contrib.auth.models import User

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'groups')
        extra_kwargs = {'password': {'write_only': True}}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_details'] = UserSerializer(instance.user).data
        return response


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_details'] = UserSerializer(instance.user).data
        return response


class NotesFullCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('title', 'date')


class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = "__all__"


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class UserSubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = "__all__"
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_details'] = UserSerializer(instance.user).data
        return response

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['subscription_details'] = SubscriptionsSerializer(instance.subscription_id).data
        return response