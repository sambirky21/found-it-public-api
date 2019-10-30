from django.db import models

# """
# Author: Sam Birky
# Purpose: Single source of information about Category Data with essential fields to be stored in database.
# This model maps to a Category database table.
# Method: None

# """

class Category(models.Model):

    name = models.CharField(max_length=50)
    __organizer_items = list()

    @property
    def organizer_items(self):
        return self.__organizer_items

    @organizer_items.setter
    def organizer_items(self, value):
        self.__organizer_items = value