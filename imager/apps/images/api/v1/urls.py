from django.urls import path

from .views import (
    ImageUrlView,
    ImageCreateView,
    ImageRetrieveUpdateView,
)


urlpatterns = [
    path('', ImageCreateView.as_view(),
         name='image-create-api-v1'),
    path('<uuid:pk>/', ImageRetrieveUpdateView.as_view(),
         name='image-retrieve-update-api-v1'),
    path('<uuid:pk>/url/', ImageUrlView.as_view(),
         name='image-url-api-v1'),
]
