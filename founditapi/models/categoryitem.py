from django.db import models
# from .item import Item
from .category import Category

"""
Author: Sam Birky
Purpose: Single source of information about Category Item Data with essential fields to be stored in database.
This model maps to a Category Item database table.
Method: None

"""
class CategoryItem(models.Model):

    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)