import datetime
import logging

from django.core.cache import cache

from management.models import GuestBook
from management.serializers import GuestBookSerializer
from utils.api import APIView, check
from utils.constans import PhotoTypeEnum

logger = logging.getLogger(__name__)


class CategoryAPI(APIView):
    def get(self, request):
        category = PhotoTypeEnum.choices()
        return self.success({'category': category})


class GuestBookAPI(APIView):
    @check(login_required=False, serializer=GuestBookSerializer)
    def post(self, request):
        data = {
            'ip_addr': request.META.get('REMOTE_ADDR'),
            'content': request.data.get('content'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'user': request.user.username
        }

        guest_book_count = cache.get('guest_book_' + data['ip_addr'])
        if guest_book_count and guest_book_count >= 10:
            return self.error('已达当日留言上限')

        now = datetime.datetime.now()
        timeout = 86400 - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second).total_seconds()
        cache.set('guest_book_' + data['ip_addr'], (guest_book_count + 1 if guest_book_count else 1), timeout=timeout)

        GuestBook.objects.create(**data)
        return self.success()
