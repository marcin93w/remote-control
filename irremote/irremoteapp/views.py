from django.shortcuts import render
from django.http import HttpResponse
from py_irsend import irsend
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

import RPi.GPIO as GPIO

import board
import neopixel

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

pixels = neopixel.NeoPixel(board.D18, 120)

def index(request):
    return render(request, 'index.html')

def send(request):
    irsend.send_once(request.GET['device'], [request.GET['button']])
    return HttpResponse('ok')

def audio_switch(request):
    source = request.GET['source']
    GPIO.output(13, source != '1')
    GPIO.output(19, source != '1')
    GPIO.output(26, source != '2')
    GPIO.output(16, source != '2')
    GPIO.output(20, source != '3')
    GPIO.output(21, source != '3')
    return HttpResponse('ok')

def hexToRgb(hex):
    h = hex.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def led(request):
    id = int(request.GET['id'])
    pixels[id] = hexToRgb(request.GET['color'])
    return HttpResponse('ok')

@csrf_exempt
def leds(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        for i, p in enumerate(data):
            if i == 59: # don't light up the one in the middle
                continue
            
            if request.GET['safeMode'] == 'true' and i % 2:
                pixels[i] = (0,0,0)
                continue

            if isinstance(p, list):
                pixels[i] = p
            else:
                pixels[i] = hexToRgb(p)
        return HttpResponse('ok')
    else: #GET
        current_state = []
        for p in pixels:
            current_state.append('#%02x%02x%02x' % (p[0], p[1], p[2]))
        return JsonResponse(current_state, safe=False)

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

