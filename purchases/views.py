import os
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, FormView
from django.core.paginator import Paginator
from users import models as user_models
from ipware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import render, HttpResponse
from . import models
from . import forms


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


class PurchaseSelectView(View):
    template_name = "purchases/purchase_select.html"

    def get(self, request):
        return render(request, "purchases/purchase_select.html")


class CreateMaterialView(FormView):
    form_class = forms.CreateMaterialForm
    template_name = "purchases/create_material.html"
    success_url = reverse_lazy("purchases/")

    def form_valid(self, form):
        title = form.cleaned_data.get("title")
        closed = form.cleaned_data.get("closed")
        price = form.cleaned_data.get("price")
        total = form.cleaned_data.get("total")
        category = form.cleaned_data.get("category")
        max_people = form.cleaned_data.get("max_people")
        explain = form.cleaned_data.get("explain")
        link_address = form.cleaned_data.get("link_address")
        user = self.request.user

        material = models.Material.objects.create(
            title=title,
            closed=closed,
            price=price,
            total=total,
            category=category,
            max_people=max_people,
            explain=explain,
            link_address=link_address,
            host=user,
            address=user.address,
        )
        material.save()
        photos = self.request.FILES.getlist("photos")
        print(photos)
        if photos is not None:
            for photo in photos:
                new_photo = models.Photo.objects.create(file=photo, purchases=material)
                new_photo.save()
        return redirect(reverse("purchases:purchase", kwargs={"pk": material.pk}))


class CreateImmaterialView(FormView):
    form_class = forms.CreateImmaterialForm
    template_name = "purchases/create_immaterial.html"
