from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from django.conf import settings

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('birthday/', include('birthday.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
