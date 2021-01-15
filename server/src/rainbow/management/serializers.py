from rest_framework import serializers


class GuestBookSerializer(serializers.Serializer):
    content = serializers.CharField()
