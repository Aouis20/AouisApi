from django.db import models


class Category(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, default=None, null=True)
