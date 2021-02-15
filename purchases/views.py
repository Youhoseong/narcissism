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
        p = models.Purchase.objects.filter(host__address=request.user.address).order_by('-pk') # 수정필요 =>  게시글에 address
        
        paginator = Paginator(p, 10)
        
        page = request.GET.get("page", 1)
        page_obj = paginator.get_page(page)
        return render(
            request, "home.html", {"page_obj": page_obj, "purchases": page_obj}
        )


class MaterialDetailView(DetailView):
    model = models.Material
    context_object_name="purchase"
    template_name = "purchases/material_detail.html"
 

    def get_context_data(self, **kwargs):
        context = super(MaterialDetailView, self).get_context_data(**kwargs)
        isIncluded = models.Material.objects.filter(participants = self.request.user.pk).exists()
        context.update({'isIncluded': isIncluded})
        return context

class ImmaterialDetailView(DetailView):
    model = models.Immaterial
    context_object_name="purchase"
    template_name = "purchases/immaterial_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ImmaterialDetailView, self).get_context_data(**kwargs)
        isIncluded = models.Immaterial.objects.filter(participants = self.request.user.pk).exists()
        context.update({'isIncluded': isIncluded})
        return context

def material_attend_view(request, pk):
    if request.method == 'GET':
        p = models.Material.objects.get(pk=pk)
        p.participants.add(request.user)
        p.save()
    return redirect(reverse("purchases:material", kwargs={'pk': pk}))

def material_delete_view(request, pk):
    if request.method == 'GET':
        p = models.Material.objects.get(pk=pk)
        p.participants.remove(request.user)
        p.save()
    return redirect(reverse("purchases:material", kwargs={'pk': pk}))

def immaterial_attend_view(request, pk):
    if request.method == 'GET':
        p = models.Immaterial.objects.get(pk=pk)
        p.participants.add(request.user)
        p.save()
    return redirect(reverse("purchases:immaterial", kwargs={'pk': pk}))

def immaterial_delete_view(request, pk):
    if request.method == 'GET':
        p = models.Immaterial.objects.get(pk=pk)
        p.participants.remove(request.user)
        p.save()
    return redirect(reverse("purchases:immaterial", kwargs={'pk': pk}))


