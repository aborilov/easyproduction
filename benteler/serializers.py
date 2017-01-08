from .models import User, Role
from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()


class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'create_time', 'role', 'url')


class RoleSerializer(BaseSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'url')
