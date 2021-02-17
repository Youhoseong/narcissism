import os
from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.gis.geoip2 import GeoIP2
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from . import models, forms

# Create your views here.

class LocationException(Exception):
    pass

class LocationVerifyDetailView(ListView):
    template_name = "users/location_verify_detail.html"
    model = models.User
    context_object_name = "users"
    lat = 1
    lon = 1
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super(LocationVerifyDetailView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        client_id = os.environ.get("KAKAO_MAP_KEY")
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")

        return render(
            request,
            "users/location_verify_detail.html",
            {
                "client_id_kakao": client_id,
                "latt": lat,
                "lonn": lon,
            },
        )

    def post(self, request, *args, **kwargs):
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")

        return redirect(reverse("core:home"))


user_create = csrf_exempt(LocationVerifyDetailView.as_view())

class LocationVerifyView(ListView):
    template_name = "users/location_verify.html"
    model = models.User
    context_object_name = "users"

    def get(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        client_id = os.environ.get("KAKAO_MAP_KEY")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        g = GeoIP2()

        return render(
            request,
            "users/location_verify.html",
            {
                "ip": ip,
                "latt": g.city("218.146.29.228").get("latitude"),
                "long": g.city("218.146.29.228").get("longitude"),
                "client_id_kakao": client_id,
            },
        )

@csrf_exempt
def verify_complete(request):
    try:
        location = request.POST.get("location")
        if location == None:
            raise LocationException()
        else:
            print(location)
            try:
                user = models.User.objects.get(pk=request.user.pk)
                print(user.username)
                user.address = location
                user.location_verified = True
                user.save()
            except models.User.DoesNotExist:
                raise LocationException()

        return redirect(reverse("core:home"))

    except LocationException as e:
        return redirect(reverse("core:home"))


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        user = self.request.user
        print(next_arg)
        print(user)
        user = models.User.objects.get(pk=self.request.user.pk)

        if user.location_verified:
            return reverse("core:home")
        else:
            return reverse("users:verify")


def log_out(request):
    messages.info(request, f"See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        user = models.User.objects.get(pk=self.request.user.pk)

        if user.location_verified:
            return reverse("core:home")
        else:
            return reverse("users:verify")


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"

class UpdateProfileView(SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "avatar",
        "email",
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "address",
        "qr_code",
    )
    succsess_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['email'].widget.attrs = {'placeholder': "email"}
        form.fields['first_name'].widget.attrs = {'placeholder': "first_name"}
        form.fields['last_name'].widget.attrs = {'placeholder': "last_name"}
        form.fields['bio'].widget.attrs = {'placeholder': "bio"}
        form.fields['birthdate'].widget.attrs = {'placeholder': "birthdate"}
        form.fields['address'].widget.attrs = {'placeholder': "address"}
        return form