import os
from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from . import models, forms
from . import mixins
from purchases import models as purchase_models
from django.views.decorators.http import require_http_methods

# Create your views here.


class LocationException(Exception):
    pass


class LocationVerifyDetailView(mixins.LoggedInOnlyView, ListView):
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
            {"client_id_kakao": client_id, "latt": lat, "lonn": lon},
        )

    def post(self, request, *args, **kwargs):
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")

        return redirect(reverse("core:home"))


user_create = csrf_exempt(LocationVerifyDetailView.as_view())


class LocationVerifyView(mixins.LoggedInOnlyView, ListView):
    template_name = "users/location_verify.html"
    model = models.User
    context_object_name = "users"

    def get(self, request):
        client_id = os.environ.get("KAKAO_MAP_KEY")

        return render(
            request, "users/location_verify.html", {"client_id_kakao": client_id}
        )


@csrf_exempt
def verify_complete(request):
    if request.method == "POST":
        try:
            user = models.User.objects.get(pk=request.user.pk)
            location = request.POST.get("location")
            temp_location = location.replace(" ", "")

            if location == None or temp_location == "":
                user.recent_location_verify_code = "0"
                user.save()
                raise LocationException()
            else:
                print(location + "앙")
                user.address = location
                user.location_verified = True
                user.recent_location_verify_code = "1"
                user.save()
                return redirect(reverse("core:home"))

        except LocationException:
            messages.error(request, "지역 업데이트 오류")
            return redirect(reverse("core:home"))

    else:
        user = models.User.objects.get(pk=request.user.pk)

        if user.recent_location_verify_code == "0":
            messages.error(request, "지역 인증에 오류가 있습니다.")
            return redirect(reverse("users:verify"))
        else:
            messages.success(request, f"{request.user.first_name}님의 지역정보를 업데이트 합니다.")
            return redirect(reverse("core:home"))


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.info(self.request, f"또 뵙네요. {self.request.user.first_name}")

        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        user = self.request.user
        user = models.User.objects.get(pk=self.request.user.pk)

        if user.location_verified:
            return reverse("core:home")
        else:
            return reverse("users:verify")


def log_out(request):
    messages.info(request, f"다음에 또 봐요, {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
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
        user.verify_email()
        return super().form_valid(form)

    def get_success_url(self):
        user = models.User.objects.get(pk=self.request.user.pk)
        messages.info(self.request, f"{self.request.user.first_name} 가입을 축하해요. ")

        if user.location_verified:
            return reverse("core:home")
        else:
            return reverse("users:verify")


class UserProfileView(mixins.LoggedInOnlyView, DetailView):
    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(SuccessMessageMixin, mixins.LoggedInOnlyView, UpdateView):
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
        "qr_code",
    )
    success_message = "프로필 새단장 완료!"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["email"].widget.attrs = {"placeholder": "email"}
        form.fields["first_name"].widget.attrs = {"placeholder": "first_name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "last_name"}
        form.fields["bio"].widget.attrs = {"placeholder": "bio"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "birthdate"}
        return form


class ShopListView(mixins.LoggedInOnlyView, ListView):
    model = models.User
    template_name = "users/list.html"

    def get(self, request):
        return render(
            request, "users/list.html", {"purchases": request.user.participate.all()}
        )


def email_verification_view(request, code):
    try:
        print(code)
        user = models.User.objects.get(email_code=code)
        user.email_verified = True
        messages.success(request, "이메일이 인증되었습니다")
        user.save()

    except models.User.DoesNotExist:
        messages.error(request, "유효하지 않은 인증입니다")

    return redirect(reverse("core:home"))
