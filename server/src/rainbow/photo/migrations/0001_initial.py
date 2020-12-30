# Generated by Django 3.1.4 on 2020-12-30 03:27

import django.contrib.postgres.fields
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('copyright', models.TextField(null=True)),
                ('category', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=list, size=None)),
                ('upload_name', models.TextField(null=True)),
                ('watch_count', models.IntegerField(default=0)),
                ('thumb_count', models.IntegerField(default=0)),
                ('download_count', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photo',
            },
        ),
    ]
