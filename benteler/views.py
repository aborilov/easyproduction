import django_filters.rest_framework

from rest_framework import viewsets, filters
from . import models

from . import serializers
from django.http import HttpResponse

import django_filters


def index(request):
    return HttpResponse("Easy Production instance for benteler")


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer


class WorkPatternViewSet(viewsets.ModelViewSet):
    queryset = models.WorkPattern.objects.all()
    serializer_class = serializers.WorkPatternSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,)
    filter_fields = ('name', 'description', 'work_type',)
    search_fields = ('name', 'description',)


class WorkViewSet(viewsets.ModelViewSet):
    queryset = models.Work.objects.all()
    serializer_class = serializers.WorkSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,)
    filter_fields = ('description', 'work_pattern', 'relevance',)
    search_fields = ('description',)


class CostCenterViewSet(viewsets.ModelViewSet):
    queryset = models.CostCenter.objects.all()
    serializer_class = serializers.CostCenterSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,)
    filter_fields = ('name', 'num',)
    search_fields = ('name',)


class PartTypeViewSet(viewsets.ModelViewSet):
    queryset = models.PartType.objects.all()
    serializer_class = serializers.PartTypeSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,)
    filter_fields = ('name',)
    search_fields = ('name',)


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = models.Manufacturer.objects.all()
    serializer_class = serializers.ManufacturerSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,)
    filter_fields = ('name',)
    search_fields = ('name',)


class PartViewSet(viewsets.ModelViewSet):
    queryset = models.Part.objects.all()
    serializer_class = serializers.PartSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,)
    filter_fields = ('name', 'manufacturer', 'code', 'part_type', 'sap_number',)
    search_fields = ('name',)


class FileViewSet(viewsets.ModelViewSet):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,)
    filter_fields = ('name', 'description',)
    search_fields = ('name', 'description',)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = models.Place.objects.all()
    serializer_class = serializers.PlaceSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,)
    filter_fields = ('name', 'serial_number', 'active', 'cost_center',
                     'parts', 'parent_place', 'files',)
    search_fields = ('name',)


class WorkTypeViewSet(viewsets.ModelViewSet):
    queryset = models.WorkType.objects.all()
    serializer_class = serializers.WorkTypeSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,)
    filter_fields = ('name', 'parent',)
    search_fields = ('name',)


class PeriodViewSet(viewsets.ModelViewSet):
    queryset = models.Period.objects.all()
    serializer_class = serializers.PeriodSerializer
    filter_fields = ('repeated', 'repeated_count',)


class EventStatusViewSet(viewsets.ModelViewSet):
    queryset = models.EventStatus.objects.all()
    serializer_class = serializers.EventStatusSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,)
    filter_fields = ('name',)
    search_fields = ('name',)


class EventViewSet(viewsets.ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter,)
    filter_fields = ('work', 'date', 'executors', 'status',)
    search_fields = ('work__description',)


class EventReportViewSet(viewsets.ModelViewSet):
    queryset = models.EventReport.objects.all()
    serializer_class = serializers.EventReportSerializer
    filter_fields = ('event', 'executor', 'description', 'work_time',
                     'down_time', 'files',)
