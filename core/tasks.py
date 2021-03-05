import logging
from background_task import background
from .models import EmailQueue

logger = logging.getLogger('django')

@background(schedule=10)
def run_queue():
    email_sending = EmailQueue.objects.filter(status='sending').first()

    if(email_sending):
        logger.debug('Rescheduling, email %s is sending.', email_sending.pk)
        run_queue()
    else:
        email_queue = EmailQueue.objects.filter(status='pending').first()

        if(email_queue):
            try:
                logger.debug('Sending email %s.', email_queue.pk)
                email_queue.send()           
                logger.debug('Email %s sent.', email_queue.pk)
            except Exception as e:
                logger.error('Error sending %s', email_queue.pk, exc_info=e)

        email_error = EmailQueue.objects.filter(status='error').first()

        if(email_error):
            logger.debug('Resending, email %s', email_error.pk)
            email_error.status = 'pending'
            run_queue()

    