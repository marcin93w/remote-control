from django.shortcuts import render
from django.http import HttpResponse
from py_irsend import irsend
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def index(request):
    return render(request, 'index.html')

def send(request):
    irsend.send_once(request.GET['device'], [request.GET['button']])
    return HttpResponse('ok')

def audio_switch(request):
    source = request.GET['source']
    GPIO.output(23, GPIO.LOW if source == 1 else GPIO.HIGH)
    GPIO.output(24, GPIO.LOW if source == 1 else GPIO.HIGH)
    GPIO.output(25, GPIO.LOW if source == 2 else GPIO.HIGH)
    GPIO.output(27, GPIO.LOW if source == 2 else GPIO.HIGH)
    GPIO.output(28, GPIO.LOW if source == 3 else GPIO.HIGH)
    GPIO.output(29, GPIO.LOW if source == 3 else GPIO.HIGH)

@csrf_exempt
def dialogflow(request):
    if request.body:
        data = json.loads(request.body.decode("utf-8"))
        if 'queryResult' in data:
            intent = data['queryResult']['intent']['displayName'] 
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
    
    return JsonResponse({
        "fulfillment_text": "unknown command"
    })

