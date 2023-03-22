from django.shortcuts import render
from django.shortcuts import HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def index(request):
    return render(request, 'video/index.html')