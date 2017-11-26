from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from django import forms
from django.db import models

from django.core.validators import validate_comma_separated_integer_list
from django.utils.encoding import python_2_unicode_compatible

from datetime import date as datetime

from enum import IntEnum

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@python_2_unicode_compatible
class UserForm(forms.ModelForm):
    class Meta:
        widgets = {'password': forms.PasswordInput()}


@python_2_unicode_compatible
class Role(models.Model):
    name = models.TextField(verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')


@python_2_unicode_compatible
class User(AbstractUser):
    role = models.ForeignKey(Role, null=True,
                             on_delete=models.CASCADE, verbose_name=_('Role'))

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


@python_2_unicode_compatible
class CostCenter(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    num = models.IntegerField(verbose_name=_('Num'))

    def __str__(self):
        return "{}:{}".format(self.name, self.num)

    class Meta:
        verbose_name = _('CostCenter')
        verbose_name_plural = _('CostCenters')


@python_2_unicode_compatible
class PartType(models.Model):
    name = models.TextField(verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('PartType')
        verbose_name_plural = _('PartTypes')


@python_2_unicode_compatible
class Manufacturer(models.Model):
    name = models.TextField(verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')


@python_2_unicode_compatible
class Part(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL,
                                     verbose_name=_('Manufacturer'),
                                     null=True, blank=True)
    code = models.TextField(verbose_name=_('Code'))
    part_type = models.ForeignKey(PartType, on_delete=models.CASCADE,
                                  verbose_name=_('PartType'))
    sap_number = models.IntegerField(verbose_name=_('SapNumber'),
                                     null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Part')
        verbose_name_plural = _('Parts')


@python_2_unicode_compatible
class File(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')


@python_2_unicode_compatible
class Place(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    serial_number = models.TextField(verbose_name=_('SerialNumber'),
                                     blank=True, null=True)
    active = models.BooleanField(default=True, verbose_name=_('Active'))
    cost_center = models.ForeignKey(CostCenter, on_delete=models.SET_NULL,
                                    verbose_name=_('CostCenter'),
                                    blank=True, null=True)
    parts = models.ManyToManyField(Part, verbose_name=_('Parts'), blank=True)
    parent_place = models.ForeignKey('Place', blank=True, null=True,
                                     verbose_name=_('ParentPlace'))
    files = models.ManyToManyField(File, verbose_name=_('Files'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')


@python_2_unicode_compatible
class WorkType(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    parent = models.ForeignKey('WorkType', blank=True, null=True,
                               verbose_name=_('ParentWorkType'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('WorkType')
        verbose_name_plural = _('WorkTypes')


@python_2_unicode_compatible
class RepeatedEnum(IntEnum):
    EveryDay = 0
    EveryWeek = 1
    EveryMonth = 2
    EveryYear = 3


@python_2_unicode_compatible
class Period(models.Model):

    repeated = models.IntegerField(
        verbose_name=_('Repeated'),
        choices=[(choice.value, choice.name) for choice in RepeatedEnum],
        #  default=RepeatedEnum.EveryDay
    )
    repeated_count = models.IntegerField(default=1,
                                         verbose_name=_('RepeatedCount'))

    def __str__(self):
        return str(RepeatedEnum(self.repeated))

    class Meta:
        verbose_name = _('Period')
        verbose_name_plural = _('Periods')


@python_2_unicode_compatible
class WorkPattern(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_('Description'))
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE,
                                  verbose_name=_('WorkType'))
    duration = models.DurationField(verbose_name=_('Duration'))
    period = models.ForeignKey(Period, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               verbose_name=_('Period'))
    child_group = models.ForeignKey('WorkPatternGroup', blank=True, null=True,
                                    verbose_name=_('ChildGroup'))
    files = models.ManyToManyField(File, verbose_name=_('Files'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('WorkPattern')
        verbose_name_plural = _('WorkPatterns')


@python_2_unicode_compatible
class WorkPatternGroup(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    child_patterns = models.ManyToManyField(WorkPattern, blank=True,
                                            verbose_name=_('ChildPatterns'))
    child_groups = models.ManyToManyField("self", blank=True,
                                          verbose_name=_('ChildPatternGroups'))
    child_order = models.TextField(
        validators=[validate_comma_separated_integer_list],
        blank=True, null=True, verbose_name=_('ChildOrder'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('WorkPatternGroup')
        verbose_name_plural = _('WorkPatternGroups')


@python_2_unicode_compatible
class Work(models.Model):
    description = models.TextField(verbose_name=_('Description'))
    work_pattern = models.ForeignKey(WorkPattern, on_delete=models.CASCADE,
                                     verbose_name=_('WorkPattern'))
    child_group = models.ForeignKey('WorkGroup', blank=True, null=True,
                                    verbose_name=_('ChildGroup'))
    place = models.ForeignKey(Place, on_delete=models.CASCADE,
                              verbose_name=_('Place'))
    parts = models.ManyToManyField(Part, blank=True,
                                   verbose_name=_('Parts'))
    date_start = models.DateField(blank=True, null=True,
                                  verbose_name=_('DateStart'))
    date_end = models.DateField(blank=True, null=True,
                                verbose_name=_('DateEnd'))
    responsibles = models.ManyToManyField(User, verbose_name=_('Responsibles'))
    relevance = models.BooleanField(default=True, verbose_name=_('Relevance'))

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Work')
        verbose_name_plural = _('Works')


@python_2_unicode_compatible
class WorkGroup(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    pattern_group = models.ForeignKey(WorkPatternGroup,
                                      on_delete=models.SET_NULL,
                                      blank=True, null=True,
                                      verbose_name=_('WorkPatternGroup'))
    child_works = models.ManyToManyField(Work, blank=True,
                                         verbose_name=_('ChildWorks'))
    child_groups = models.ManyToManyField("self", blank=True,
                                          verbose_name=_('ChildWorkGroups'))
    child_order = models.TextField(
        validators=[validate_comma_separated_integer_list],
        blank=True, null=True, verbose_name=_('ChildOrder'))
    visibility = models.BooleanField(verbose_name=_('Visibility'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('WorkGroup')
        verbose_name_plural = _('WorkGroups')


@python_2_unicode_compatible
class EventStatus(models.Model):
    name = models.TextField(verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('EventStatus')
        verbose_name_plural = _('EventStatuses')


@python_2_unicode_compatible
class Event(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE,
                             verbose_name=_('Work'))
    date = models.DateField(default=datetime.today,
                            verbose_name=_('Date'))
    executors = models.ManyToManyField(User, verbose_name=_('Executors'))
    status = models.ForeignKey(EventStatus, on_delete=models.CASCADE,
                               verbose_name=_('EventStatus'))

    def __str__(self):
        return self.work.work_pattern.name

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


@python_2_unicode_compatible
class EventReport(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              verbose_name=_('Event'))
    executor = models.ForeignKey(User, on_delete=models.CASCADE,
                                 verbose_name=_('Executor'))
    description = models.TextField(verbose_name=_('Description'))
    work_time = models.DurationField(verbose_name=_('WorkTime'))
    down_time = models.DurationField(verbose_name=_('DownTime'))
    files = models.ManyToManyField(File, verbose_name=_('Files'), blank=True)

    def __str__(self):
        return "{} [{}]".format(self.event.work.work_pattern.name,
                                self.executor.username)

    class Meta:
        verbose_name = _('EventReport')
        verbose_name_plural = _('EventReports')
