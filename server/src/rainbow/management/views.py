import logging
from utils.api import APIView
from utils.constans import PhotoTypeEnum

logger = logging.getLogger(__name__)


class CategoryAPI(APIView):
    def get(self, request):
        category = PhotoTypeEnum.choices()
        return self.success({'category': category})

