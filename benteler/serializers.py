from . import models
from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()


class UserSerializer(BaseSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'email', 'create_time', 'role', 'url')


class RoleSerializer(BaseSerializer):
    class Meta:
        model = models.Role
        fields = ('id', 'name', 'url')


class WorkPatternSerializer(BaseSerializer):
    class Meta:
        model = models.WorkPattern
        fields = ('id', 'name', 'description', 'url', 'work_type', 'duration',
                  'period', 'child_group', 'files')


class WorkSerializer(BaseSerializer):
    class Meta:
        model = models.Work
        fields = ('id', 'description', 'url', 'work_pattern', 'date_start',
                  'date_end', 'responsibles', 'relevance')


class CostCenterSerializer(BaseSerializer):
    class Meta:
        model = models.CostCenter
        fields = ('id', 'url', 'name', 'num')


class PartTypeSerializer(BaseSerializer):
    class Meta:
        model = models.PartType
        fields = ('id', 'url', 'name')


class ManufacturerSerializer(BaseSerializer):
    class Meta:
        model = models.Manufacturer
        fields = ('id', 'url', 'name')


class PartSerializer(BaseSerializer):
    class Meta:
        model = models.Part
        fields = ('id', 'url', 'name', 'manufacturer', 'code', 'part_type',
                  'sap_number')


class FileSerializer(BaseSerializer):
    class Meta:
        model = models.File
        fields = ('id', 'url', 'name', 'description',)


class PlaceSerializer(BaseSerializer):
    class Meta:
        model = models.Place
        fields = ('id', 'url', 'name', 'serial_number', 'active', 'cost_center',
                  'parts', 'parent_place', 'files')


class WorkTypeSerializer(BaseSerializer):
    class Meta:
        model = models.WorkType
        fields = ('id', 'url', 'name', 'parent',)


class PeriodSerializer(BaseSerializer):
    class Meta:
        model = models.Period
        fields = ('id', 'url', 'repeated', 'repeated_count',)


class WorkPatternGroupSerializer(BaseSerializer):
    class Meta:
        model = models.WorkPatternGroup
        fields = ('id', 'url', 'name', 'child_patterns', 'child_groups',
                  'child_order',)


class WorkGroupSerializer(BaseSerializer):
    class Meta:
        model = models.WorkGroup
        fields = ('id', 'url', 'name', 'pattern_group', 'child_works',
                  'child_groups', 'child_order', 'visibility')


class EventStatusSerializer(BaseSerializer):
    class Meta:
        model = models.EventStatus
        fields = ('id', 'url', 'name')


class EventSerializer(BaseSerializer):
    class Meta:
        model = models.Event
        fields = ('id', 'url', 'work', 'date', 'executors', 'status')


class EventReportSerializer(BaseSerializer):
    class Meta:
        model = models.EventReport
        fields = ('id', 'url', 'event', 'executor', 'description', 'work_time',
                  'down_time', 'files')
