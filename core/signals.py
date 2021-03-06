import logging

from django.dispatch import receiver
from django.db.models.signals import post_save
from core.models import EmailQueue, Template

logger = logging.getLogger('django')

@receiver(post_save, sender=EmailQueue)
def create_response_email(sender, instance, created, **kwargs):
    if(created):
        print(instance.template.slug)
        print('portfolio_contact')
        if(instance.template.slug=='portfolio_contact'):
            template_slug = 'portfolio_contact_response'
            template = Template.objects.get(slug=template_slug)

            email_queue = EmailQueue.objects.create(
                template=template, 
                email_from='admin@reciclatusanimales.com', 
                email_name=instance.email_name, 
                email_to=instance.email_from, 
                subject='Contacto Reciclatusanimales', 
                content='Hola'
            )

            email_queue.save()