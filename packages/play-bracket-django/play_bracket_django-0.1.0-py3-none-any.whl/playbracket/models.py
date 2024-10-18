from django.db import models


class Event(models.Model):
    date = models.DateField(null=False, blank=False)


class Match(models.Model):
    date = models.DateField(null=False, blank=False)
    cleared = models.BooleanField(default=False)


class Player(models.Model):
    name = models.CharField(max_length=80, blank=False, null=False, unique=True)


class Sport(models.Model):
    name = models.CharField(max_length=80, blank=False, null=False, unique=True)


class League(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False)
