import logging

from django.core.management.base import BaseCommand

from management.models import Config
from utils.constans import ConfigEnum

logger = logging.getLogger(__name__)


def update_or_create_config():
    for key in ConfigEnum.choices():
        try:
            Config.objects.get(key=key)
        except Config.DoesNotExist:
            Config.objects.create(key=key)


class Command(BaseCommand):
    help = "Init Server Config"

    def handle(self, *args, **options):
        update_or_create_config()
