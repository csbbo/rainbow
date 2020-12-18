from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=32)


class RegistSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=32)
    email = serializers.EmailField(max_length=100, required=False)
    tel = serializers.CharField(max_length=11, min_length=11, required=False)
