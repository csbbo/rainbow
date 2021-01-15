import logging
from functools import reduce
from operator import or_

from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q

from photo.models import Photo
from photo.serializers import PhotoSerializer, CreatePhotoSerializer
from utils.api import APIView, check
from utils.serializers import UUIDOnlySerializer, UUIDListSerializer, UploadFileForm
from utils.shortcuts import rand_str, datetime_pretty, save_file

logger = logging.getLogger(__name__)


class PhotoAPI(APIView):
    @check(login_required=False, serializer=UUIDOnlySerializer)
    def get(self, request):
        id = request.data['id']
        try:
            photo = Photo.objects.get(id=id)
        except Photo.DoesNotExist:
            return self.error('photo not exists')
        data = PhotoSerializer(photo).data
        return self.success(data)

    @check(permission='__all__', serializer=CreatePhotoSerializer)
    def post(self, request):
        user = request.user
        data = request.data

        data['user'] = user
        photo = Photo.objects.create(**data)
        return self.success({'id': str(photo.id)})

    @check(permission='__all__', serializer=UUIDListSerializer)
    def delete(self, request):
        ids = request.data['ids']
        photos = Photo.objects.filter(id__in=ids)
        if len(photos) != len(ids):
            return self.error('删除对象不存在或重复!')
        photos.delete()
        return self.success()


class PhotoListAPI(APIView):
    @check(login_required=False)
    def get(self, request):
        data = request.data
        category = data.getlist('category', [])
        search = data.get('search')

        if len(category) > 0:
            photos = Photo.objects.filter(reduce(or_, (Q(category__contains=[cat, ]) for cat in category))).order_by('-create_time')
        elif search:
            photos = Photo.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search) | Q(copyright__icontains=search)).order_by('-create_time')
        else:
            photos = Photo.objects.all()

        data = self.paginate_data(photos, object_serializer=PhotoSerializer, force=True)
        return self.success(data)


class UploadPhotoAPI(APIView):
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
            save_file(save_name, file, path=settings.PHOTOS_PATH)
            return self.success({'upload_name': upload_name, 'save_name': save_name})
        except Exception as e:
            logger.error(e)
            return self.error('图片存储失败!')


class DownloadPhotoAPI(APIView):
    @check(login_required=False, serializer=UUIDOnlySerializer)
    def get(self, request):
        id = request.data['id']
        try:
            photo = Photo.objects.get(id=id)
        except Photo.DoesNotExist:
            return self.error('图片不存在!')

        download_name = f"rainbow_{datetime_pretty(fmt='%Y%m%d')}_{rand_str(length=8)}.jpg"
        return self.download_photo(download_name=download_name, save_name=photo.save_name)


class ThumbPhotoAPI(APIView):
    @check(login_required=False, serializer=UUIDOnlySerializer)
    def post(self, request):
        id = request.data['id']
        client_ip = request.META['REMOTE_ADDR']
        cache_ip = cache.get('thumb_' + id)
        if cache_ip and cache_ip == client_ip:
            return self.error('一天只能点赞一次!')

        with transaction.atomic():
            try:
                photo = Photo.objects.select_for_update().get(id=id)
            except Photo.DoesNotExist:
                return self.error('图片不存在!')
            photo.thumb_count += 1
            photo.save()

        cache.set('thumb_' + id, client_ip, timeout=60*60*24)
        return self.success()


class WatchPhotoAPI(APIView):
    @check(login_required=False, serializer=UUIDOnlySerializer)
    def post(self, request):
        id = request.data['id']
        with transaction.atomic():
            try:
                photo = Photo.objects.select_for_update().get(id=id)
            except Photo.DoesNotExist:
                return self.error('图片不存在!')
            photo.watch_count += 1
            photo.save()
        return self.success()
