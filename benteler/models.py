from __future__ import unicode_literals

from django import forms
from django.db import models


class UserForm(forms.ModelForm):
    class Meta:
        widgets = {'password': forms.PasswordInput()}


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class CostCenter(models.Model):
    name = models.CharField(max_length=255)
    num = models.IntegerField()

    def __str__(self):
        return "{}:{}".format(self.name, self.num)


class PartType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Part(models.Model):
    name = models.CharField(max_length=255)
    # May be we need to use separate model for manufacturers
    manufacturer = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    part_type = models.ForeignKey(PartType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    cost_center = models.ForeignKey(CostCenter, on_delete=models.CASCADE)
    parts = models.ManyToManyField(Part)

    def __str__(self):
        return self.name


class WorkType(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('WorkType', blank=True, null=True)

    def __str__(self):
        return self.name


