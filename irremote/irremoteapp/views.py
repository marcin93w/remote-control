from django.shortcuts import render
from django.http import HttpResponse
from py_irsend import irsend
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def send(request):
    irsend.send_once(request.GET['device'], [request.GET['button']])
    return HttpResponse('ok')

@csrf_exempt
def dialogflow(request):
    if request.body:
        if request.body.queryResult:
            intent = request.body.queryResult.intent.displayName 
            if intent == 'radio-on':
                irsend.send_once('radio', ['aux'])
            elif intent == 'radio-off':
                irsend.send_once('radio', ['power'])
            elif intent == 'tv':
                irsend.send_once('tv', ['power'])
            elif intent == 'channel-next':
                irsend.send_once('tv', ['ch-up'])
            elif intent == 'channel-prev':
                irsend.send_once('tv', ['ch-down'])

            return JsonResponse({
                "fulfillment_text": "ok"
            })
    else:
        return JsonResponse({
        "fulfillment_text": "unknown command"
    })

