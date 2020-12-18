import logging

from django.contrib import auth
from django.contrib.sessions.models import Session
from django.db import transaction
from django.utils import timezone

from account.models import User
from account.serializers import LoginSerializer, RegistSerializer
from utils.api import APIView, check
from utils.constans import UserTypeEnum

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
                return self.error('username not exist')

            user = auth.authenticate(username=username, password=password)
            if not user:
                return self.error('password error')

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

        if User.object.filter(username=data['username']).exists():
            return self.error('username is exists')

        if tel and User.object.filter(tel=tel).exists():
            return self.error('tel is exists')

        if email and User.object.filter(email=email).exists():
            return self.error('email is exists')

        del data['password']
        user = User.object.create(**data)
        user.set_password(password)
        user.user_type = UserTypeEnum.user
        user.save()
        return self.success()
