import logging

from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger('django')


class App(models.Model):
    name = models.CharField(max_length=255)
    directory = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Template(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='templates')
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)
    filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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
    email_to = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField()
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

        BaseMailer(
            subject=self.subject,
            content=self.content,
            email_from=self.email_from,
            email_to=[self.email_to],
            template=self.template.filename
        ).send_email()

        self.status = 'sent'
        self.save()
        return

class BaseMailer():
    def __init__(self, email_from, email_to, subject, content, template, html_content=""):
        self.email_from = email_from
        self.email_to = email_to
        self.subject = subject
        self.content = content
        self.html_content = html_content
        self.template = 'core/' + template
        
    def send_email(self):
        try:
            context = {"from": self.email_from, "subject": self.subject, "content": self.content}
            self.html_content = render_to_string(self.template, context)
            send_mail(
                subject=self.subject,
                message=self.content,
                html_message=self.html_content,
                from_email=self.email_from,
                recipient_list=[self.email_to],
                fail_silently=False,
            )            
            return True
        except Exception as e:
            logger.error('Error at %s', 'register view', exc_info=e)            
            return False