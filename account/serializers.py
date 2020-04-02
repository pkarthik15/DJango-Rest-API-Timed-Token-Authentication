from django.contrib.auth.models import User as DJUser
from rest_framework import serializers
from account.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = DJUser
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'last_login', 'date_joined']