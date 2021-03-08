from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from core.views import home, add_email, run_queue

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('add-email', add_email, name="add_email"),
    path('run-queue', run_queue, name="run_queue"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "EMAIL Admin Panel"
admin.site.site_title = "EMAIL App Admin"
admin.site.site_index_title = "Welcome to EMAIL Admin Panel"