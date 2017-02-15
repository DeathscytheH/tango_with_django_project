from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    return HttpResponse("Rango says hello! Check our <a href='/rango/about'>about</a> page")


def about(request):
    return HttpResponse("Rango says here is the about page. Retun to <a href='/'> home </a> page.")
