from django.shortcuts import render
from django.http import HttpResponse
from py_irsend import irsend
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(28, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)

def index(request):
    return render(request, 'index.html')

def send(request):
    irsend.send_once(request.GET['device'], [request.GET['button']])
    return HttpResponse('ok')

def audio_switch(request):
    source = request.GET['source']
    GPIO.output(23, source == 1)
    GPIO.output(24, source == 1)
    GPIO.output(25, source == 2)
    GPIO.output(27, source == 2)
    GPIO.output(28, source == 3)
    GPIO.output(29, source == 3)

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

