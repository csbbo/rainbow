from rest_framework import serializers

from photo.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    img_path = serializers.SerializerMethodField()

    def get_img_path(self, obj):
        return '/_/photo/' + obj.save_name

    class Meta:
        model = Photo
        fields = '__all__'


class CreatePhotoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=40, required=False)
    description = serializers.CharField(max_length=200, required=False)

    copyright = serializers.CharField(max_length=200, required=False)
    category = serializers.ListField(child=serializers.CharField(max_length=10), required=False)

    save_name = serializers.CharField(max_length=64)
    upload_name = serializers.CharField(max_length=200)
