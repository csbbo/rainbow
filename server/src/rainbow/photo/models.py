import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(null=True)
    description = models.TextField(null=True)

    copyright = models.TextField(null=True)
    category = ArrayField(models.CharField(max_length=32), default=list)

    save_name = models.CharField(max_length=32)
    upload_name = models.TextField(null=True)

    watch_count = models.IntegerField(default=0)
    thumb_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)

    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = verbose_name
