import re

from rest_framework import serializers

from account.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=32)


class RegistSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=32)
    email = serializers.EmailField(max_length=100, required=False)
    tel = serializers.CharField(max_length=11, min_length=11, required=False)
    captcha = serializers.CharField(max_length=4, min_length=4)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'tel', 'user_type', 'last_login_time', 'create_time')


class UpdateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32, required=False)
    email = serializers.EmailField(max_length=100, required=False)
    tel = serializers.CharField(max_length=11, min_length=11, required=False)


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, phone):
        pattern = re.compile(r'^1(3|4|5|6|7|8|9)\d{9}$')
        if not pattern.match(phone):
            raise serializers.ValidationError('mobile phone format error')
        return phone


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
