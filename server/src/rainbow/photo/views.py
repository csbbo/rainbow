import logging
from functools import reduce
from operator import or_

from django.db.models import Q

from photo.models import Photo
from photo.serializers import PhotoListSerializer
from utils.api import APIView, check
from utils.serializers import UUIDOnlySerializer, UUIDListSerializer

logger = logging.getLogger(__name__)


class PhotoAPI(APIView):
    @check(permission='__all__', serializer=UUIDOnlySerializer)
    def get(self, request):
        id = request.data['id']
        try:
            photo = Photo.objects.get(id=id)
        except Photo.DoesNotExist:
            return self.error('photo not exists')
        data = {
            'id': id,
            'name': photo.name,
            'description': photo.description,
            'copyright': photo.copyright,
            'category': photo.category,

            'watch_num': photo.watch_num,
            'thumb_num': photo.thumb_num,
            'download_num': photo.download_num,

            'create_time': photo.create_time,
            'update_time': photo.update_time,
        }
        return self.success(data)

    @check(permission='__all__', serializer=UUIDListSerializer)
    def delete(self, request):
        ids = request.data['ids']
        photos = Photo.objects.filter(id__in=ids)
        if len(photos) != len(ids):
            return self.error('please check the photo exists and not repeat')
        photos.delete()
        return self.success()


class PhotoListAPI(APIView):
    def get(self, request):
        data = request.data
        category = data.getlist('category', [])
        search = data.get('search')

        if len(category) > 0:
            photos = Photo.objects.filter(reduce(or_, (Q(category__contains=[cat, ]) for cat in category)))
        elif search:
            photos = Photo.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search) | Q(copyright__icontains=search))
        else:
            photos = Photo.objects.all()

        data = self.paginate_data(photos, object_serializer=PhotoListSerializer, force=True)
        return self.success(data)


class UploadPhotoAPI(APIView):
    def post(self, request):
        pass
