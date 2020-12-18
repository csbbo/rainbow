import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    copyright = models.CharField(max_length=100, null=True)
    category = ArrayField(models.CharField(max_length=20), default=list)

    watch_num = models.IntegerField(default=0)
    thumb_num = models.IntegerField(default=0)
    download_num = models.IntegerField(default=0)

    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = verbose_name
