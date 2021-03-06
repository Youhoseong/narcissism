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

        if p.participants.count() == p.max_people:
            alarm_views.participant_full(request, p)
            p.status = models.Purchase.status_recruite_end
        p.save()
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

        if p.participants.count() == p.max_people:
            alarm_views.participant_full(request, p)
            p.status = models.Purchase.status_recruite_end

        p.save()
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


class CreateMaterialView(
    SuccessMessageMixin,
    mixins.LoggedInOnlyView,
    mixins.LocationVerifiedOnlyView,
    FormView,
):
    form_class = forms.CreateMaterialForm
    template_name = "purchases/create_material.html"

    def form_valid(self, form):
        title = form.cleaned_data.get("title")
        closed = form.cleaned_data.get("closed")
        price = form.cleaned_data.get("price")
        unit = form.cleaned_data.get("unit")
        category = form.cleaned_data.get("category")
        max_people = form.cleaned_data.get("max_people")
        explain = form.cleaned_data.get("explain")
        link_address = form.cleaned_data.get("link_address")
        user = self.request.user
        material = models.Material.objects.create(
            title=title,
            closed=closed,
            price=price,
            unit=unit,
            category=category,
            max_people=max_people,
            explain=explain,
            link_address=link_address,
            host=user,
            address=user.address,
        )
        material.participants.add(user)
        material.save()
        photos = self.request.FILES.getlist("photos")
        if photos is not None:
            for photo in photos:
                new_photo = models.Photo.objects.create(file=photo, purchases=material)
                new_photo.save()
        messages.success(self.request, "게시물 업로드 완료")
        return redirect(reverse("purchases:material", kwargs={"pk": material.pk}))


class CreateImmaterialView(
    SuccessMessageMixin,
    mixins.LocationVerifiedOnlyView,
    mixins.LoggedInOnlyView,
    FormView,
):
    form_class = forms.CreateImmaterialForm
    template_name = "purchases/create_immaterial.html"

    def form_valid(self, form):
        immaterial = form.save()
        user = self.request.user
        immaterial.host = user
        immaterial.address = user.address
        immaterial.save()
        immaterial.participants.add(user)
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


class SearchView(mixins.LoggedInOnlyView, View):
    def get(self, request):
        kwd = request.GET.get("kwd")

        if kwd == "":
            purchase_object = None
            purchase_count = 0

        else:
            purchase_object = models.Purchase.objects.filter(
                title__icontains=kwd, address=request.user.address
            )
            purchase_count = purchase_object.count()

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
        
        return redirect(reverse("core:home"))


class EditMaterialView(SuccessMessageMixin, mixins.LoggedInOnlyView, UpdateView):
    model = models.Material
    form_class = forms.EditMaterialForm
    template_name = "purchases/material_edit.html"
    success_message = "수정 완료"

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        material = models.Material.objects.get(pk=pk)
        if material.status != purchase_models.Purchase.status_ongoing:
            messages.error(request, "진행 중인 글만 수정할 수 있습니다.")
            return redirect(reverse("purchases:material", kwargs={"pk": pk}))
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        material = super().get_object(queryset=queryset)
        if material.host.pk == self.request.user.pk:
            return material
        else:
            raise Http404()

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        material = models.Material.objects.get(pk=pk)
        if material.status != purchase_models.Purchase.status_ongoing:
            return redirect(reverse("purchases:material", kwargs={"pk": pk}))
        photos = self.request.FILES.getlist("photos")
        if photos is not None:
            for photo in photos:
                new_photo = models.Photo.objects.create(file=photo, purchases=material)
                new_photo.save()
        return super().form_valid(form)


class EditImmaterialView(SuccessMessageMixin, mixins.LoggedInOnlyView, UpdateView):
    model = models.Immaterial
    template_name = "purchases/immaterial_edit.html"
    success_message = "수정 완료"
    form_class = forms.EditImaterialForm

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        immaterial = models.Immaterial.objects.get(pk=pk)
        if immaterial.status != purchase_models.Purchase.status_ongoing:
            messages.error(request, "진행 중인 글만 수정할 수 있습니다.")
            return redirect(reverse("purchases:immaterial", kwargs={"pk": pk}))
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        immaterial = super().get_object(queryset=queryset)
        if immaterial.host.pk == self.request.user.pk:
            return immaterial
        else:
            raise Http404()

    def form_valid(self, form):
        photos = self.request.FILES.getlist("photos")
        pk = self.kwargs["pk"]
        immaterial = models.Immaterial.objects.get(pk=pk)
        print(pk)
        if photos is not None:
            for photo in photos:
                new_photo = models.Photo.objects.create(
                    file=photo, purchases=immaterial
                )
                new_photo.save()
        return super().form_valid(form)


def delete_photo_view(request, pk):
    if request.method == "GET":
        photo = models.Photo.objects.get(pk=pk)
        messages.success(request, "사진 삭제 완료")
        photo.delete()
        next = request.GET["next"]
        return redirect(next)


def material_close_view(request, pk):
    if request.method == "GET":
        p = models.Material.objects.get(pk=pk)
        if p.host.pk == request.user.pk:
            p.status = models.Purchase.status_finished
            p.save()
        else:
            raise Http404()

        messages.success(request, "공동구매 모집 마감 완료!")
    return redirect(reverse("purchases:material", kwargs={"pk": pk}))


def immaterial_close_view(request, pk):
    if request.method == "GET":
        p = models.Immaterial.objects.get(pk=pk)
        if p.host.pk == request.user.pk:
            p.status = models.Purchase.status_finished
            p.save()
        else:
            raise Http404()

        messages.success(request, "공동구매 모집 마감 완료!")
    return redirect(reverse("purchases:immaterial", kwargs={"pk": pk}))
