import logging

from django.dispatch import receiver
from django.db.models.signals import post_save
from core.models import EmailQueue, Template
from .constants import default_sender

logger = logging.getLogger('django')

@receiver(post_save, sender=EmailQueue)
def create_response_email(sender, instance, created, **kwargs):
    if(created):
        if(instance.template.response):
            email_queue = EmailQueue.objects.create(
                template=instance.template.response, 
                email_from=default_sender, 
                email_name=instance.email_name, 
                email_to=instance.email_from, 
                subject=instance.template.response.subject, 
                content=''
            )

            email_queue.save()