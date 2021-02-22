import os
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, FormView, UpdateView
from django.core.paginator import Paginator
from users import models as user_models
from comments import models as comment_models
from purchases import models as purchase_models
from comments import models as comment_models
from comments import forms as comment_forms
from django.urls import reverse_lazy
from ipware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import render, HttpResponse
from . import models
from . import forms
from users import mixins
from alarms import views as alarm_views

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

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
        p = models.Purchase.objects.filter(address=request.user.address).order_by(
            "-pk"
        )  # 수정필요 =>  게시글에 address

        paginator = Paginator(p, 10)
        page = request.GET.get("page", 1)
        page_obj = paginator.get_page(page)
        return render(
            request, "home.html", {"page_obj": page_obj, "purchases": page_obj}
        )


class MaterialDetailView(mixins.LoggedInOnlyView, mixins.SameAreaOnlyView, DetailView):
    model = models.Material
    context_object_name = "purchase"
    template_name = "purchases/material_detail.html"

    def get_context_data(self, **kwargs):
        context = super(MaterialDetailView, self).get_context_data(**kwargs)
        isIncluded = models.Material.objects.filter(
            pk=self.kwargs["pk"], participants=self.request.user.pk
        ).exists()
        form = comment_forms.CommentForm
        context.update({"isIncluded": isIncluded, "form": form})
        return context

    def post(self, request, *args, **kwargs):
        context = request.POST.get("comment")
        user = user_models.User.objects.get(pk=request.user.pk)
        purchase_pk = kwargs["pk"]

        purchase_obj = purchase_models.Purchase.objects.get(pk=purchase_pk)

        comment_obj = comment_models.Comment.objects.create(
            context=context, writer=user, purchase=purchase_obj
        )
        comment_obj.save()
        messages.success(request, "댓글 업로드 완료!")
        return redirect(reverse("purchases:material", kwargs={"pk": purchase_pk}))


class ImmaterialDetailView(
    mixins.LoggedInOnlyView, mixins.SameAreaOnlyView, DetailView
):
    model = models.Immaterial
    context_object_name = "purchase"
    template_name = "purchases/immaterial_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ImmaterialDetailView, self).get_context_data(**kwargs)
        print(self.kwargs["pk"])
        isIncluded = models.Immaterial.objects.filter(
            pk=self.kwargs["pk"], participants=self.request.user.pk
        ).exists()
        form = comment_forms.CommentForm
        context.update({"isIncluded": isIncluded, "form": form})
        print(isIncluded)
        return context

    def post(self, request, *args, **kwargs):
        context = request.POST.get("comment")
        user = user_models.User.objects.get(pk=request.user.pk)
        purchase_pk = kwargs["pk"]

        purchase_obj = purchase_models.Purchase.objects.get(pk=purchase_pk)

        comment_obj = comment_models.Comment.objects.create(
            context=context, writer=user, purchase=purchase_obj
        )
        comment_obj.save()
        messages.success(request, "댓글 업로드 완료!")
        return redirect(reverse("purchases:immaterial", kwargs={"pk": purchase_pk}))


def material_attend_view(request, pk):
    if request.method == "GET":
        p = models.Material.objects.get(pk=pk)
        p.participants.add(request.user)
        p.save()

        if p.participants.count() == p.max_people:
            alarm_views.participant_full(request, p)
        messages.success(request, "공동구매 참여 완료!")
    return redirect(reverse("purchases:material", kwargs={"pk": pk}))


def material_delete_view(request, pk):
    if request.method == "GET":
        p = models.Material.objects.get(pk=pk)
        p.participants.remove(request.user)
        p.save()
        messages.success(request, "공동구매 취소 완료!")
    return redirect(reverse("purchases:material", kwargs={"pk": pk}))


def immaterial_attend_view(request, pk):
    if request.method == "GET":
        p = models.Immaterial.objects.get(pk=pk)
        p.participants.add(request.user)
        p.save()

        if p.participants.count() == p.max_people:
            alarm_views.participant_full(request, p)
        messages.success(request, "공동구매 참여 완료!")
    return redirect(reverse("purchases:immaterial", kwargs={"pk": pk}))


def immaterial_delete_view(request, pk):
    if request.method == "GET":
        p = models.Immaterial.objects.get(pk=pk)
        p.participants.remove(request.user)
        p.save()
        messages.success(request, "공동구매 참여 취소 완료!")
    return redirect(reverse("purchases:immaterial", kwargs={"pk": pk}))


class PurchaseDetailView(mixins.LoggedInOnlyView, DetailView):
    model = models.Purchase
    template_name = "purchases/purchase_detail.html"


class CreateMaterialView(SuccessMessageMixin, mixins.LoggedInOnlyView, FormView):
    form_class = forms.CreateMaterialForm
    template_name = "purchases/create_material.html"

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
        if photos is not None:
            for photo in photos:
                new_photo = models.Photo.objects.create(file=photo, purchases=material)
                new_photo.save()
        messages.success(self.request, "게시물 업로드 완료")
        return redirect(reverse("purchases:material", kwargs={"pk": material.pk}))


class CreateImmaterialView(SuccessMessageMixin, mixins.LoggedInOnlyView, FormView):
    form_class = forms.CreateImmaterialForm
    template_name = "purchases/create_immaterial.html"

    def form_valid(self, form):
        immaterial = form.save()
        user = self.request.user
        immaterial.host = user
        immaterial.address = user.address
        immaterial.save()
        form.save_m2m()
        photos = self.request.FILES.getlist("photos")
        if photos is not None:
            for photo in photos:
                new_photo = models.Photo.objects.create(
                    file=photo, purchases=immaterial
                )
                new_photo.save()
        messages.success(self.request, "게시물 업로드 완료")
        return redirect(reverse("purchases:immaterial", kwargs={"pk": immaterial.pk}))


class SearchView(View):
    def get(self, request):
        kwd = request.GET.get("kwd")

        if kwd == "":
            purchase_object = 0
            purchase_count = 0

        else:
            purchase_object = models.Purchase.objects.filter(
                title__icontains=kwd, address=request.user.address
            )
            purchase_count = purchase_object.count()

        # category에 의한 검색도 하고싶으나... 객체가 달라서 ㅠㅠ

        return render(
            request,
            "purchases/search.html",
            {"purchases": purchase_object, "purchases_count": purchase_count},
        )


def purchase_delete_view(request, pk):
    if request.method == "GET":
        try:
            p = models.Material.objects.get(pk=pk)
        except models.Material.DoesNotExist:
            p = models.Immaterial.objects.get(pk=pk)
        messages.success(request, "게시글 삭제 완료")
        p.delete()
        next = request.GET["next"]
        return redirect(next)


class EditMaterialView(SuccessMessageMixin, mixins.LoggedInOnlyView, UpdateView):
    model = models.Material
    template_name = "purchases/material_edit.html"
    success_message = "수정 완료"
    fields = (
        "title",
        "category",
        "closed",
        "max_people",
        "price",
        "total",
        "unit",
        "explain",
        "link_address",
    )

    def get_object(self, queryset=None):
        material = super().get_object(queryset=queryset)
        if material.host.pk == self.request.user.pk:
            return material
        else:
            raise Http404()


class EditImmaterialView(SuccessMessageMixin, mixins.LoggedInOnlyView, UpdateView):
    model = models.Immaterial
    template_name = "purchases/immaterial_edit.html"
    success_message = "수정 완료"
    fields = {"title", "closed", "explain", "category", "max_people", "price"}

    def get_object(self, queryset=None):
        immaterial = super().get_object(queryset=queryset)
        if immaterial.host.pk == self.request.user.pk:
            return immaterial
        else:
            raise Http404()
