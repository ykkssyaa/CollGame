from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic import RedirectView

from games.views import page_not_found
from users.views import terms

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('games.urls')),
    path('terms/', terms, name='terms'),
    path('users/', include(('users.urls', 'users'))),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("img/gamepad.ico")), name="favicon")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
