from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
Author: Sam Birky
Purpose: Single source of information about Organzier Data with essential fields to be stored in database.
This model maps to a Organizer database table.
Method: None

"""

class Organizer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=25)