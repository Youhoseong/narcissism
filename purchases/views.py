from django.shortcuts import render
from django.views.generic import ListView
from . import models
from ipware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import render, HttpResponse
import os
# Create your views here.


class HomeView(ListView):
    """ HomeView Definition """
    model = models.Purchase
    template_name = "home.html"
    context_object_name = "purchases"
   
    
    def get(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        client_id = os.environ.get("CLIENT_ID_NAVER_MAP")
        print(client_id)
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

            g = GeoIP2()
            print(g.country('naver.com'))
        

        return render(request, "home.html", {
            "ip": ip,
            "client_id_naver": client_id,
        }) 

# FBV home definition 이해를 위해 남겨둠.

""" 
def home(request):
    x_forwarded_for = request.META['HTTP_X_FORWARDED_FOR']
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    return HttpResponse("Welcome Home<br>You are visiting from: {}".format(ip)) """