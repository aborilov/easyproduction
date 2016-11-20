from .models import User, Role
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'create_time', 'role', 'url')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('name', 'url')
