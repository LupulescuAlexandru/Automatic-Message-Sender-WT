from django.urls import path, re_path
from .views import view_images
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('view_images/', view_images, name="view-images"),
    #re_path(r'view_image/(?P<imageid>\w+)/$', view_image, name="view-image"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
