from django.http import JsonResponse

def api_response(json_object):
    return JsonResponse(json_object, safe=False, json_dumps_params={'ensure_ascii': False})