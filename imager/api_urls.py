from django.urls import path, include

from .apps.images.api.v1 import urls as images_api_urls

urlpatterns = [
    path('v1/images/', include(images_api_urls)),
]
