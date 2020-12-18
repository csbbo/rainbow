from rest_framework import serializers

from photo.models import Photo


class PhotoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = '__all__'
