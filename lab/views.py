from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseNotAllowed,HttpResponseBadRequest
# Create your views here.


def home(request):
    return HttpResponse(render(request, 'home.html'))