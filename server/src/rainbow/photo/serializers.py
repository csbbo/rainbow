from rest_framework import serializers

from photo.models import Photo


class PhotoListSerializer(serializers.ModelSerializer):
    img_path = serializers.SerializerMethodField()

    def get_img_path(self, obj):
        return '/_/photo/' + str(obj.id)

    class Meta:
        model = Photo
        fields = '__all__'
