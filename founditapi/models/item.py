from django.db import models
from django.contrib.auth.models import User

"""
Author: Sam Birky
Purpose: Single source of information about Item Data with essential fields to be stored in database.
This model maps to a Item database table.
Method: None

"""

class Item(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)