import logging

from django.conf import settings
from django.core.cache import cache

from management.models import GuestBook
from management.serializers import GuestBookSerializer, CreateGuestBookSerializer
from utils.api import APIView, check
from utils.constans import PhotoTypeEnum
from utils.serializers import UploadFileForm
from utils.shortcuts import end_of_day_seconds, rand_str, save_file

logger = logging.getLogger(__name__)


class CategoryAPI(APIView):
    def get(self, request):
        category = PhotoTypeEnum.choices()
        return self.success({'category': category})


class GuestBookAPI(APIView):
    @check(login_required=False)
    def get(self, request):
        guest_books = GuestBook.objects.all()
        data = GuestBookSerializer(guest_books, many=True).data
        return self.success(data)

    @check(login_required=False, serializer=CreateGuestBookSerializer)
    def post(self, request):
        data = {
            'ip_addr': request.META.get('REMOTE_ADDR'),
            'content': request.data.get('content'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'user': request.user.username if request.user.username else None
        }

        guest_book_count = cache.get('guest_book_' + data['ip_addr'])
        if guest_book_count and guest_book_count >= 10:
            return self.error('已达当日留言上限')

        cache.set('guest_book_' + data['ip_addr'],
                  (guest_book_count + 1 if guest_book_count else 1),
                  timeout=end_of_day_seconds())

        GuestBook.objects.create(**data)
        return self.success()


class UploadFileAPI(APIView):
    request_header = ()

    @check(permission='__all__')
    def post(self, request):
        upload_file_form = UploadFileForm(request.POST, request.FILES)
        if not upload_file_form.is_valid():
            return self.error(msg='文件上传失败!')

        file = request.FILES['file']
        upload_name = file.name.split('.')[0]
        save_name = rand_str(length=32)

        try:
            save_file(save_name, file, path=settings.DOWNLOAD_PATH)
        except Exception as e:
            logger.error(e)
            return self.error('文件上传失败!')

        return self.success({'upload_name': upload_name, 'save_name': save_name})
