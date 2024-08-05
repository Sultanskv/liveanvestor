# myapp/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['client_code', 'jwt_token', 'refresh_token', 'feed_token']

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'userprofile']


# -------------------------------------------------------------------------
# ==========================================================================
from rest_framework import serializers

from client_api.models import ind_clientDT

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ind_clientDT
        fields = '__all__'
