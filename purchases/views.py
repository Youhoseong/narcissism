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
    paginate_by = 10
    paginate_orphans = 4
    ordering = "-created"
    context_object_name = "purchases"
    template_name = "home.html"


def Participate(request):
    model = models.Purchase
    user = request.user
    model.participants.add(user)
