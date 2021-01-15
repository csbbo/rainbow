class Choices:
    @classmethod
    def choices(cls, *, exclude_field=()):
        d = cls.__dict__
        ret = {str(d[item]) for item in d.keys() if not item.startswith("_")}
        return list(ret - set(exclude_field))


class ConfigEnum(Choices):
    EMAIL_ADDR = 'EMAIL_ADDR'
    EMAIL_SMTP_SERVER = 'EMAIL_SMTP_SERVER'
    EMAIL_PORT = 'EMAIL_PORT'
    EMAIL_PASSWORD = 'EMAIL_PASSWORD'


class PhotoTypeEnum(Choices):
    bing = "必应"
    anime = "动漫"
    landscape = '风景'


class UserTypeEnum(Choices):
    user = 'user'
    super_admin = 'super_admin'
