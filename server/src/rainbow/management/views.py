import logging

from django.core.cache import cache

from management.models import GuestBook
from management.serializers import GuestBookSerializer
from photo.models import Photo
from photo.serializers import PhotoSerializer
from utils.api import APIView, check
from utils.constans import PhotoTypeEnum
from utils.shortcuts import end_of_day_seconds

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

        cache.set('guest_book_' + data['ip_addr'],
                  (guest_book_count + 1 if guest_book_count else 1),
                  timeout=end_of_day_seconds())

        GuestBook.objects.create(**data)
        return self.success()


class MainPageAPI(APIView):
    @check(login_required=False)
    def get(self, request):
        bing_newest_photo = Photo.objects.filter(category__contains=[PhotoTypeEnum.bing, ]).order_by('-create_time').first()
        bing_photo = PhotoSerializer(bing_newest_photo).data
        return self.success({'bing': bing_photo})
