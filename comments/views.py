from django.shortcuts import render, reverse, redirect
from . import models
from django.contrib import messages

# Create your views here.

def comment_delete_view(request, pk):
    if request.method == "GET":
        p = models.Comment.objects.get(pk=pk)
        purchase_pk = p.purchase.pk
        p.delete()
    messages.success(request, "댓글 삭제 완료!")
    return redirect(reverse("purchases:material", kwargs={"pk": purchase_pk}))