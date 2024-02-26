from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic import RedirectView

from games.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('games.urls')),
    path('', include('users.urls')),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("img/gamepad.ico")), name="favicon")
]

handler404 = page_not_found
