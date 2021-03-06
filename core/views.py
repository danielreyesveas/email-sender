import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt      
from .utils import api_response                                    
from .models import EmailQueue, Template
from .constants import default_recipients

from .tasks import run_queue

def home(request):
    return HttpResponse("Hello friend...")

@csrf_exempt 
def add_email(request):
    json_response = {
        'success': False
    }

    try:
        if(not request.body): 
            json_response['msg'] = 'Sin datos' 
            return api_response(json_response)

        data = json.loads(request.body.decode("utf-8"))

        if('subject' not in data): 
            json_response['msg'] = 'El campo \'subject\' no puede estar vacío' 
            return api_response(json_response)
        elif('from' not in data): 
            json_response['msg'] = 'El campo \'from\' no puede estar vacío' 
            return api_response(json_response)
        elif('content' not in data): 
            json_response['msg'] = 'El campo \'content\' no puede estar vacío' 
            return api_response(json_response)
        elif('template_slug' not in data): 
            json_response['msg'] = 'El campo \'template_slug\' no puede estar vacío' 
            return api_response(json_response)
        
        subject = data['subject']
        email_from = data['from']
        content = data['content']

        if('name' in data): 
            email_name = data['name']
        else:
            email_name = None
        
        if('to' in data): 
            email_to = data['to']
        else:
            email_to = default_recipients

        try:
            template = Template.objects.get(slug=data['template_slug'])
        except Template.DoesNotExist:
            template = None

        if(template is None): 
            json_response['msg'] = 'La plantilla no existe' 
            return api_response(json_response)

        email_queue = EmailQueue.objects.create(
            template=template, 
            email_from=email_from, 
            email_name=email_name, 
            email_to=email_to, 
            subject=subject, 
            content=content
        )

        email_queue.save()

        json_response['success'] = True

        run_queue()

        return api_response(json_response)
    except Exception as e:
        json_response['msg'] = 'Hubo un problema'
        json_response['error'] = e
        
        return api_response(json_response)