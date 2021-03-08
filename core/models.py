import logging

from django.db import models
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .constants import default_sender, default_recipients

import core
import binascii
import os

logger = logging.getLogger('django')


class App(models.Model):
    name = models.CharField(max_length=255)
    directory = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ApiKey(models.Model):
    key = models.CharField(max_length=32, blank=True, null=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='api_keys')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ApiKey, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(16)).decode()

    def __unicode__(self):
        return self.key

class Template(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='templates')
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)
    filename = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True, null=True)
    response = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

class EmailQueue(models.Model):
    STATUS = [
        ('pending', 'Pendiente'),
        ('sending', 'Enviando'),
        ('sent', 'Enviado'),
        ('error', 'Error'),
        ('cancel', 'Cancelado'),
    ]

    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='emails')
    email_from = models.CharField(max_length=255)
    email_name = models.CharField(max_length=255, blank=True, null=True)
    email_to = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_email_queue'

    def __str__(self):
        return self.subject    

    def send(self):

        self.status = 'sending'
        self.save()

        try:
            BaseMailer(
                subject=self.subject,
                content=self.content,
                email_name=self.email_name,
                email_from=self.email_from,
                email_to=self.email_to,
                email_subject=self.template.subject,
                template=self.template.filename
            ).send_email()
            self.status = 'sent'    

        except Exception as e:
            self.status = 'error'
            self.save()
            core.tasks.run_queue()           
        
        self.save()
        return

class BaseMailer():
    def __init__(self, email_from, email_to, email_subject, subject, content, template, email_name, html_content=""):
        self.email_from = email_from
        self.email_name = email_name
        self.email_to = email_to
        self.email_subject = email_subject
        self.subject = subject
        self.content = content
        self.html_content = html_content
        self.template = 'core/' + template
        
    def send_email(self):
        
        context = {"from": self.email_from, "name": self.email_name, "to": self.email_to, "subject": self.subject, "content": self.content}
        self.html_content = render_to_string(self.template, context)

        email = EmailMessage(
            self.email_subject,
            self.html_content,
            default_sender,
            [self.email_to],
            [default_recipients]
        )
        email.content_subtype = "html"        
        email.send()     
