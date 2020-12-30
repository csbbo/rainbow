import errno
import functools
import json
import logging
import typing
from urllib.parse import quote

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, QueryDict
from django.views.generic.base import View

logger = logging.getLogger(__name__)


class ContentType:
    json_request = "application/json"
    json_response = "application/json;charset=UTF-8"
    url_encoded_request = "application/x-www-form-urlencoded"
    binary_response = "application/octet-stream"


class Response:
    @classmethod
    def response(cls, data, status):
        resp = JsonResponse(data, status=status)
        resp.data = data
        return resp


class APIError(Exception):
    def __init__(self, msg: str, *, err: str = "error"):
        self.err = err
        self.msg = msg
        super().__init__(err, msg)


class APIView(View):
    response_class = Response
    request_header = (ContentType.json_request, ContentType.url_encoded_request)

    def _get_request_data(self):
        if self.request.method != "GET":
            body = self.request.body
            content_type = self.request.META.get("CONTENT_TYPE")
            if not content_type:
                raise ValueError("content_type is required")

            if content_type.startswith(ContentType.json_request):
                return json.loads(body.decode("utf-8"))
            elif content_type.startswith(ContentType.url_encoded_request):
                return QueryDict(body)
            else:
                raise ValueError(f"unknown content_type '{content_type}'")
        return self.request.GET

    def response(self, data: typing.Union[list, dict, int, float, str], *, status: int = 200):
        resp = self.response_class.response(data, status=status)
        return resp

    def success(self, data: typing.Union[list, dict, int, float, str] = None, status: int = 200):
        return self.response({"err": None, "data": data}, status=status)

    def error(self, msg: str, *, err: str = "error", status: int = 200):
        return self.response({"err": err, "msg": msg}, status=status)

    def server_error(self):
        return self.error(err="server-error", msg="服务器错误")

    def login_required(self):
        return self.error(err="login-required", msg="需要登录", status=401)

    def extract_errors(self, errors, key="field"):
        if isinstance(errors, dict):
            if not errors:
                return key, "Invalid field"
            key = list(errors.keys())[0]
            return self.extract_errors(errors.pop(key), key)
        elif isinstance(errors, list):
            return self.extract_errors(errors[0], key)

        return key, errors

    def invalid_serializer(self, serializer):
        key, error = self.extract_errors(serializer.errors)
        if key == "non_field_errors":
            msg = error
        else:
            msg = f"{error}"
        return self.error(err=f"invalid-{key}", msg=msg)

    def download_photo(self, download_name, save_name):
        resp = self.success()
        resp['X-Accel-Redirect'] = f'/_/photo/{save_name}'
        resp['Content-Disposition'] = f"inline; filename*=UTF-8''{quote(download_name)}"
        resp['Content-Type'] = 'application/octet-stream'
        return resp

    def paginate_data(self, query_set, object_serializer=None, force=False, context=None):
        need_paginate = self.request.GET.get("count", None)
        if need_paginate is None:
            if force:
                raise APIError("'count' is required")
            if object_serializer:
                return object_serializer(query_set, many=True).data
            else:
                return query_set
        try:
            limit = int(self.request.GET.get("count", "100"))
        except ValueError:
            limit = 100
        if limit < 0:
            limit = 100
        try:
            offset = int(self.request.GET.get("offset", "0"))
        except ValueError:
            offset = 0
        if offset < 0:
            offset = 0
        results = query_set[offset:offset + limit]
        if object_serializer:
            count = query_set.count() if not isinstance(query_set, list) else len(query_set)
            results = object_serializer(results, many=True, context=context).data if context \
                else object_serializer(results, many=True).data
        else:
            count = len(query_set)
        data = {"items": results,
                "total": count}
        return data

    def dispatch(self, request, *args, **kwargs):
        if self.request_header:
            request.data = self._get_request_data()

        try:
            return super(APIView, self).dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist as e:
            logger.exception(e)
            return self.object_does_not_exist(str(e).split(" ", maxsplit=1)[0])
        except APIError as e:
            return self.error(err=e.err, msg=e.msg)
        except OSError as e:
            if e.errno == errno.ENOSPC:
                return self.error(msg="硬盘已满，请联系管理员")
            logger.exception(e)
            return self.server_error()
        except Exception as e:
            logger.exception(e)
            return self.server_error()


class check:
    def __init__(self, permission=None, *, serializer=None, serializer_many=False,
                 login_required=True, license_required=True):
        self.permission = permission
        self.serializer = serializer
        self.serializer_many = serializer_many
        self.login_required = login_required
        self.license_required = license_required

        if (serializer_many and not serializer) or (permission and not login_required):
            raise ValueError("Invalid check condition")

    def _check_permission(self, request):
        if self.permission is None:
            return False

        if self.permission == '__all__':
            return True

        user_type = request.user.user_type

        if user_type in self.permission:
            return True
        else:
            return False

    def _get_current_user(self, request):
        user = request.user
        if user.is_authenticated:
            return user
        return None

    def __call__(self, fn):
        @functools.wraps(fn)
        def _check(*args, **kwargs):
            func_self = args[0]
            request = args[1]

            if self.login_required:
                user = self._get_current_user(request)
                if not user:
                    return func_self.login_required()
                request.user = user

                if not self._check_permission(request):
                    return func_self.permission_denied()
            if self.serializer:
                s = self.serializer(data=request.data, many=self.serializer_many)
                if s.is_valid():
                    request.data = s.data
                    request.serializer = self.serializer
                else:
                    return func_self.invalid_serializer(s)
            return fn(*args, **kwargs)
        return _check
