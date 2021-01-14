from django.db import models


class Config(models.Model):
    key = models.TextField(unique=True, db_index=True)
    value = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
