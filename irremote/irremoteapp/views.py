from django.shortcuts import render
from django.http import HttpResponse
from py_irsend import irsend

def index(request):
    return render(request, 'index.html')

def send(request):
    irsend.send_once(request.GET['device'], [request.GET['button']])
    return HttpResponse('ok')
