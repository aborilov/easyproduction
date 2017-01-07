from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from django import forms
from django.db import models


class UserForm(forms.ModelForm):
    class Meta:
        widgets = {'password': forms.PasswordInput()}


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')


class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class CostCenter(models.Model):
    name = models.CharField(max_length=255)
    num = models.IntegerField()

    def __str__(self):
        return "{}:{}".format(self.name, self.num)

    class Meta:
        verbose_name = _('CostCenter')
        verbose_name_plural = _('CostCenters')


class PartType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('PartType')
        verbose_name_plural = _('PartTypes')


class Part(models.Model):
    name = models.CharField(max_length=255)
    # May be we need to use separate model for manufacturers
    manufacturer = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    part_type = models.ForeignKey(PartType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Part')
        verbose_name_plural = _('Parts')

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
   
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')

class Place(models.Model):
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    cost_center = models.ForeignKey(CostCenter, on_delete=models.CASCADE)
    parts = models.ManyToManyField(Part)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')


class WorkType(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('WorkType', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('WorkType')
        verbose_name_plural = _('WorkTypes')
