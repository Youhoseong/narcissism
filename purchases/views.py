from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView
from . import models
from users import models as user_models
from ipware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import render, HttpResponse
import os


import requests
# Create your views here.


class HomeView(ListView):
    """ HomeView Definition """
    model = models.Purchase
    template_name = "home.html"
    context_object_name = "purchases"
  
    def get(self, request):
        # response = requests.get('https://ncloud.apigw.ntruss.com/geolocation/v1').json()
        # print(response)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        client_id = os.environ.get("KAKAO_MAP_KEY")

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        g = GeoIP2()

        return render(request, "home.html", {
            "ip": ip,
            "latt": g.city('218.146.29.228').get('latitude'),
            "long": g.city('218.146.29.228').get('longitude'),
            "client_id_kakao": client_id,
        }) 

    def post(self, request):
        location = request.POST.get('location')
        print(location)
        # user = user_models.User.objects.get(pk=request.user.pk)
        # user.address = location
        # user.save()

        return redirect(reverse("core:home"))

# user pk 추가해야함 => login 추가 후
def create_user_location(request):
    location = request.POST['location']
    print(location)

    return redirect(reverse("core:home"))
    
    

