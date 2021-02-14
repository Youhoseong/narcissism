import os
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from users import models as user_models
from ipware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import render, HttpResponse
from . import models


import requests

# Create your views here.


class HomeView(ListView):
    """ HomeView Definition """

    # 이전처럼 지역에 상관없이 보여주려면 아래 주석된 부분을 없애고 get을 주석처리해주면 됩니다
    """
    model = models.Purchase
    paginate_by = 8
    paginate_orphans = 0
    ordering = "-created"
    context_object_name = "purchases"
    template_name = "home.html"
    """

    def get(self, request):
        if request.user.is_anonymous:
            return render(request, "home.html")
        p = models.Purchase.objects.filter(host__address=request.user.address)
        paginator = Paginator(p, 10)
        page = request.GET.get("page", 1)
        page_obj = paginator.get_page(page)
        return render(
            request, "home.html", {"page_obj": page_obj, "purchases": page_obj}
        )


def Participate(request):
    model = models.Purchase
    user = request.user
    model.participants.add(user)


class PurchaseDetailView(DetailView):
    model = models.Purchase
    template_name = "purchases/purchase_detail.html"
