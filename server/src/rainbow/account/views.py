import logging

from django.contrib import auth
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from account.models import User
from account.serializers import LoginSerializer, RegistSerializer, PhoneSerializer, EmailSerializer
from management.utils import send_email_captcha
from utils.api import APIView, check
from utils.constans import UserTypeEnum
from utils.shortcuts import rand_str

logger = logging.getLogger(__name__)


class LoginAPI(APIView):
    @check(login_required=False, serializer=LoginSerializer)
    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']

        with transaction.atomic():
            try:
                User.object.select_for_update().get(username=username)
            except User.DoesNotExist:
                return self.error('用户不存在!')

            user = auth.authenticate(username=username, password=password)
            if not user:
                return self.error('密码错误!')

            auth.login(request=request, user=user)
            user.last_login_time = timezone.now()
            user.save()

            # single sign on
            session_list = Session.objects.exclude(session_key=request.session.session_key)
            for session in session_list:
                session_data = session.get_decoded()
                if session_data.get('_auth_user_id') == str(user.id):
                    session.delete()
            return self.success()


class RegistAPI(APIView):
    @check(login_required=False, serializer=RegistSerializer)
    def post(self, request):
        data = request.data
        password = data['password']
        tel = data.get('tel', None)
        email = data.get('email', None)
        captcha = data.get('captcha')

        if captcha != cache.get(email):
            return self.error('验证码错误!')

        if User.object.filter(username=data['username']).exists():
            return self.error('该用户名已注册!')

        if tel and User.object.filter(tel=tel).exists():
            return self.error('该手机号已注册!')

        if email and User.object.filter(email=email).exists():
            return self.error('该邮箱已注册!')

        del data['password']
        del data['captcha']
        user = User.object.create(**data)
        user.set_password(password)
        user.user_type = UserTypeEnum.user
        user.save()
        return self.success()


class LogoutAPI(APIView):
    def post(self, request):
        auth.logout(request)
        return self.success()


class AuthInfoAPI(APIView):
    @check(login_required=True, permission='__all__')
    def get(self, request):
        user = request.user
        data = {
            'username': user.username
        }
        return self.success(data)


# not use
class PhoneCaptchaAPI(APIView):
    @check(login_required=False, serializer=PhoneSerializer)
    def get(self, request):
        phone = request.data['phone']
        if cache.get('captcha_' + phone):
            return self.error('at least 120s between captcha application')

        captcha = rand_str(length=4, type='lower_hex')
        cache.set('captcha_' + phone, captcha, timeout=120)
        # send_phone_captcha
        return self.success()


class EmailCaptchaAPI(APIView):
    @check(login_required=False, serializer=EmailSerializer)
    def get(self, request):
        email = request.data['email']
        # if cache.get('captcha_' + email):
        #     return self.error('at least 120s between captcha application')

        captcha = rand_str(length=4, type='lower_hex')
        cache.set('captcha_' + email, captcha, timeout=120)
        is_success = send_email_captcha(email, captcha)
        if not is_success:
            return self.error('发送失败!')
        return self.success()
