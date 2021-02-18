from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from purchases import models as purchase_models


class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "이미 로그인 되어있습니다")
        return redirect("core:home")


class SameAreaOnlyView(UserPassesTestMixin):
    def test_func(self):
        pk = self.kwargs["pk"]
        address = purchase_models.Purchase.objects.get(pk=pk).address
        if address == self.request.user.address:
            return True
        else:
            return False

    def handle_no_permission(self):
        messages.error(self.request, "다른 지역이거나 지역 인증이 완료되지 않았습니다.")
        return redirect("core:home")


class LocationVerifiedOnlyView(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.location_verified:
            return True
        else:
            return False

    def handle_no_permission(self):
        messages.error(self.request, "지역인증 후 이용해주시기 바랍니다.")
        return redirect("users:verify")


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")
