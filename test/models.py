from __future__ import unicode_literals
from django.db import models
from django_pendulum_field.fields import PendulumField


class User(models.Model):
    first_name = models.CharField(max_length=100)
    creation_date = PendulumField()


class UserAutoNow(models.Model):
    first_name = models.CharField(max_length=100)
    creation_date = PendulumField(auto_now=True)


class UserAutoNowAdd(models.Model):
    first_name = models.CharField(max_length=100)
    creation_date = PendulumField(auto_now_add=True)
