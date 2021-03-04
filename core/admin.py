from django.contrib import admin
from .models import App, Template, EmailQueue

class AppAdmin(admin.ModelAdmin):
    list_display = ['name', 'directory',]

class TemplateAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'app', 'filename']

class EmailQueueAdmin(admin.ModelAdmin):
    list_display = ['email_from', 'email_to', 'subject', 'template', 'status']

admin.site.register(App, AppAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(EmailQueue, EmailQueueAdmin)