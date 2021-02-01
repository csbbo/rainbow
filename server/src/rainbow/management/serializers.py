from rest_framework import serializers

from management.models import GuestBook


class GuestBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = GuestBook
        fields = '__all__'


class CreateGuestBookSerializer(serializers.Serializer):
    content = serializers.CharField()


