from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from django import forms
from django.db import models

from django.core.validators import validate_comma_separated_integer_list

from datetime import date as datetime


class UserForm(forms.ModelForm):
    class Meta:
        widgets = {'password': forms.PasswordInput()}


@python_2_unicode_compatible
class Role(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')


@python_2_unicode_compatible
class User(models.Model):
    username = models.CharField(max_length=255, verbose_name=_('UserName'))
    email = models.EmailField(verbose_name=_('Email'))
    password = models.CharField(max_length=32, verbose_name=_('Password'))
    create_time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_('CreateTime'))
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name=_('Role'))

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


@python_2_unicode_compatible
class CostCenter(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    num = models.IntegerField(verbose_name=_('Num'))

    def __str__(self):
        return "{}:{}".format(self.name, self.num)

    class Meta:
        verbose_name = _('CostCenter')
        verbose_name_plural = _('CostCenters')


@python_2_unicode_compatible
class PartType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('PartType')
        verbose_name_plural = _('PartTypes')

@python_2_unicode_compatible
class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')

@python_2_unicode_compatible
class Part(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name=_('Manufacturer'))
    code = models.CharField(max_length=255, verbose_name=_('Code'))
    part_type = models.ForeignKey(PartType, on_delete=models.CASCADE, verbose_name=_('PartType'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Part')
        verbose_name_plural = _('Parts')


@python_2_unicode_compatible
class Place(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    serial_number = models.CharField(max_length=255, verbose_name=_('SerialNumber'), blank=True)
    active = models.BooleanField(default=True, verbose_name=_('Active'))
    cost_center = models.ForeignKey(CostCenter, on_delete=models.CASCADE, verbose_name=_('CostCenter'), blank=True, null=True )
    parts = models.ManyToManyField(Part, verbose_name=_('Parts'), blank=True)
    parent_place = models.ForeignKey('Place', blank=True, null=True, verbose_name=_('ParentPlace'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')


@python_2_unicode_compatible
class WorkType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    parent = models.ForeignKey('WorkType', blank=True, null=True, verbose_name=_('ParentWorkType'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('WorkType')
        verbose_name_plural = _('WorkTypes')


@python_2_unicode_compatible
class WorkPattern(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.CharField(max_length=255, verbose_name=_('Description'), blank=True)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE, verbose_name=_('WorkType'))
    duration = models.IntegerField(verbose_name=_('Duration'), blank=True)
    period = models.IntegerField(verbose_name=_('Period'), blank=True)
    child_group = models.ForeignKey('WorkPatternGroup', blank=True, null=True, verbose_name=_('ChildGroup'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('WorkPattern')
        verbose_name_plural = _('WorkPatterns')


@python_2_unicode_compatible
class WorkPatternGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    child_patterns = models.ManyToManyField(WorkPattern, blank=True, verbose_name=_('ChildPatterns'))
    child_groups = models.ManyToManyField("self", blank=True, verbose_name=_('ChildPatternGroups'))
    child_order = models.CharField(max_length=255, validators=[validate_comma_separated_integer_list],
                                   blank=True, null=True, verbose_name=_('ChildOrder'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('WorkPatternGroup')
        verbose_name_plural = _('WorkPatternGroups')


@python_2_unicode_compatible
class Work(models.Model):
    description = models.CharField(max_length=255, verbose_name=_('Description'))
    work_pattern = models.ForeignKey(WorkPattern, on_delete=models.CASCADE, null=False, blank=False,
                                     verbose_name=_('WorkPattern'))
    child_group = models.ForeignKey('WorkGroup', blank=True, null=True, verbose_name=_('ChildGroup'))
    place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=False, null=False, verbose_name=_('Place'))
    part = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Part'))
    date_start = models.DateField(blank=True, null=True, verbose_name=_('DateStart'))
    date_end = models.DateField(blank=True, null=True, verbose_name=_('DateEnd'))
    responsibles = models.ManyToManyField(User, blank=False, verbose_name=_('Responsibles'))
    relevance = models.BooleanField(default=True, verbose_name=_('Relevance'))

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Work')
        verbose_name_plural = _('Works')


@python_2_unicode_compatible
class WorkGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    pattern_group = models.ForeignKey(WorkPatternGroup, on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name=_('WorkPatternGroup'))
    child_works = models.ManyToManyField(Work, blank=True, verbose_name=_('ChildWorks'))
    child_groups = models.ManyToManyField("self", blank=True, verbose_name=_('ChildWorkGroups'))
    child_order = models.CharField(max_length=255, validators=[validate_comma_separated_integer_list],
                                   blank=True, null=True, verbose_name=_('ChildOrder'))
    visibility = models.BooleanField(verbose_name=_('Visibility'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('WorkGroup')
        verbose_name_plural = _('WorkGroups')


@python_2_unicode_compatible
class EventStatus(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('EventStatus')
        verbose_name_plural = _('EventStatuses')


@python_2_unicode_compatible
class Event(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, blank=False, null=False, verbose_name=_('Work'))
    date = models.DateField(default=datetime.today, blank=False, null=False, verbose_name=_('Date'))
    executors = models.ManyToManyField(User, blank=False, verbose_name=_('Executors'))
    status = models.ForeignKey(EventStatus, on_delete=models.CASCADE, blank=False, null=False,
                               verbose_name=_('EventStatus'))

    def __str__(self):
        return self.work.work_pattern.name

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')