from rest_framework import serializers


class UUIDOnlySerializer(serializers.Serializer):
    """
    只需要传递 UUID
    """
    id = serializers.UUIDField()


class UUIDListSerializer(serializers.Serializer):
    """
    只需要传递多个 ID
    """
    ids = serializers.ListField(child=serializers.UUIDField(), allow_empty=False)
