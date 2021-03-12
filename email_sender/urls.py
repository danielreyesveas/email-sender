from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from core.views import home, send_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('send-email', send_email, name="send_email"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "EMAIL Admin Panel"
admin.site.site_title = "EMAIL App Admin"
admin.site.site_index_title = "Welcome to EMAIL Admin Panel"