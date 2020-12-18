class Choices:
    @classmethod
    def choices(cls, *, exclude_field=()):
        d = cls.__dict__
        ret = {str(d[item]) for item in d.keys() if not item.startswith("_")}
        return list(ret - set(exclude_field))


class PhotoTypeEnum(Choices):
    bing = "bing"
    infinity = "infinity"
    anime = "anime"
    landscape = 'landscape'


class UserTypeEnum(Choices):
    user = 'user'
    super_admin = 'super_admin'
