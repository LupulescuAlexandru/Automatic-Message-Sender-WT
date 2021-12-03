from django.urls import path, re_path
from .views import add_image_view, view_images, delete_image
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('add_image/', add_image_view),
    path('view_images/', view_images, name="view-images"),
    re_path(r'^delete_image/(?P<imageid>\w+)/$', delete_image, name="delete-image"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
