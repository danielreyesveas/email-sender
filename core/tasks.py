import logging
from core.models import EmailQueue
from background_task import background
from background_task.models import Task


logger = logging.getLogger('django')

@background(schedule=5)
def run_queue():
    email_sending = EmailQueue.objects.filter(status='sending').first()
    available_tasks = (Task.objects.count() < 10)

    if(email_sending and available_tasks):
        logger.debug('Rescheduling, email %s is sending.', email_sending.pk)
        run_queue()
        return
    else:
        email_queues = EmailQueue.objects.filter(status='pending').count()        

        if(email_queues > 1 and available_tasks):
            run_queue()
        
        email_queue = EmailQueue.objects.filter(status='pending').first()

        if(email_queue):
            try:
                logger.info('Sending email %s.', email_queue.pk)
                email_queue.send()           
                logger.info('Email %s sent.', email_queue.pk)
            except Exception as e:
                logger.error('Error sending %s', email_queue.pk, exc_info=e)

    email_error = EmailQueue.objects.filter(status='error').first()

    if(email_error):
        logger.debug('Resending, email %s', email_error.pk)
        email_error.status = 'pending'
        email_error.save()

        if(available_tasks):
            run_queue()        

    