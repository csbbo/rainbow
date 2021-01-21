import logging
import os
from functools import reduce
from operator import or_

import cv2
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q

from photo.models import Photo, PhotoCheck
from photo.serializers import PhotoSerializer, CreatePhotoSerializer, PublishPhotoSerializer
from photo.utils import to_sketch, to_cartoon
from utils.api import APIView, check
from utils.serializers import UUIDOnlySerializer, UUIDListSerializer
from utils.shortcuts import rand_str, datetime_pretty, end_of_day_seconds

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
            photos = Photo.objects.order_by('-create_time')

        data = self.paginate_data(photos, object_serializer=PhotoSerializer, force=True)
        return self.success(data)


class PublishPhotoAPI(APIView):
    @check(permission='__all__', serializer=PublishPhotoSerializer)
    def post(self, request):
        pass


class DownloadPhotoAPI(APIView):
    @check(login_required=False, serializer=UUIDOnlySerializer)
    def post(self, request):
        id = request.data['id']
        try:
            photo = Photo.objects.get(id=id)
        except Photo.DoesNotExist:
            return self.error('图片不存在!')

        download_name = f"rainbow_{datetime_pretty(fmt='%Y%m%d')}_{rand_str(length=8)}.jpg"
        return self.download_image(download_name=download_name, save_name=photo.save_name)


class DownloadGrayPhotoAPI(APIView):
    @check(login_required=False, serializer=UUIDOnlySerializer)
    def post(self, request):
        id = request.data['id']
        try:
            photo = Photo.objects.get(id=id)
        except Photo.DoesNotExist:
            return self.error('图片不存在!')

        image = cv2.imread(os.path.join(settings.PHOTOS_PATH, photo.save_name))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        stream = cv2.imencode('.jpg', gray)[1].tobytes()
        filename = f"rainbow_gray_{datetime_pretty(fmt='%Y%m%d')}_{rand_str(length=8)}.jpg"
        return self.response_stream(stream, filename=filename)


class DownloadSketchPhotoAPI(APIView):
    @check(login_required=False, serializer=UUIDOnlySerializer)
    def post(self, request):
        id = request.data['id']
        try:
            photo = Photo.objects.get(id=id)
        except Photo.DoesNotExist:
            return self.error('图片不存在!')

        image = cv2.imread(os.path.join(settings.PHOTOS_PATH, photo.save_name))
        sketch = to_sketch(image)
        stream = cv2.imencode('.jpg', sketch)[1].tobytes()
        filename = f"rainbow_sketch_{datetime_pretty(fmt='%Y%m%d')}_{rand_str(length=8)}.jpg"
        return self.response_stream(stream, filename)


class DownloadCartoonPhotoAPI(APIView):
    @check(login_required=False, serializer=UUIDOnlySerializer)
    def post(self, request):
        id = request.data['id']
        try:
            photo = Photo.objects.get(id=id)
        except Photo.DoesNotExist:
            return self.error('图片不存在!')

        image = cv2.imread(os.path.join(settings.PHOTOS_PATH, photo.save_name))
        cartoon = to_cartoon(image)
        stream = cv2.imencode('.jpg', cartoon)[1].tobytes()
        filename = f"rainbow_cartoon_{datetime_pretty(fmt='%Y%m%d')}_{rand_str(length=8)}.jpg"
        return self.response_stream(stream, filename)


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

        cache.set('thumb_' + id, client_ip, timeout=end_of_day_seconds())
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
