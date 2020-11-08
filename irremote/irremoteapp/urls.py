from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('send', views.send, name='send'),
    path('audioswitch', views.audio_switch, name='audioswitch'),
    path('led', views.led, name='led'),
    path('leds', views.leds, name='leds'),
    path('dialogflow', views.dialogflow, name='dialogflow'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)