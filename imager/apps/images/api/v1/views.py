from django.conf import settings
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)

from imager.apps.images.models import Image
from .serializers import (
    ImageCreateSerializer,
    ImageExportSerializer,
    ImageUrlSerializer,
    ImageSerializer
)


class ImageUrlView(RetrieveAPIView):
    serializer_class = ImageUrlSerializer
    queryset = Image.objects.all()


class ImageCreateView(CreateAPIView):
    serializer_class = ImageCreateSerializer
    queryset = Image.objects.all()


class ImageRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Image.objects.all()

    @property
    def is_internal(self):
        if self.request.method != 'GET':
            return True

        return self.request.query_params.get('format', 'export') == 'internal'

    def get_serializer_class(self):
        if self.is_internal:
            return ImageSerializer

        return ImageExportSerializer
