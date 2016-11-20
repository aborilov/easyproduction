from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Role

from .serializers import UserSerializer, RoleSerializer
from django.http import HttpResponse


def index(request):
    return HttpResponse("Easy Production instance for benteler")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
