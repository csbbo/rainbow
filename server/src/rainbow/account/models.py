from django.contrib.auth.models import AbstractBaseUser, UserManager as AbstractUserManager
from django.db import models

from utils.constans import UserTypeEnum


class UserManager(AbstractUserManager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        return self.get(username=username)

    def create_superuser(self, username, password, email=None, **extra_fields):
        extra_fields.setdefault('user_type', UserTypeEnum.super_admin)
        if extra_fields.get('user_type') != UserTypeEnum.super_admin:
            raise ValueError('Superuser must have user_type=%s.' % UserTypeEnum.super_admin)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")
    username = models.TextField(unique=True)
    password = models.TextField()

    email = models.TextField(null=True)
    tel = models.CharField(null=True, max_length=11)

    user_type = models.TextField(default=UserTypeEnum.user)

    last_login_time = models.DateTimeField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    object = UserManager()

    def has_perm(self, perm, obj=None):
        """
        user是否拥有perm权限
        """
        return True

    def has_module_perms(self, app_label):
        """
        user是否拥有app中访问models的权限
        """
        return True

    @property
    def is_staff(self):
        """
        user访问admin页面权限
        """
        return self.user_type == UserTypeEnum.super_admin

    class Meta:
        db_table = 'user'
        ordering = ['id']
