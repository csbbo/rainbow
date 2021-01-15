from django.contrib.postgres.fields import ArrayField
from django.db import models


class Config(models.Model):
    key = models.TextField(unique=True, db_index=True)
    value = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class GuestBook(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    ip_addr = models.TextField()
    content = models.TextField()
    user_agent = models.TextField(null=True)
    user = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
