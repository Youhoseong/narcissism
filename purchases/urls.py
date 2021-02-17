from django.contrib import admin
from django.urls import path
from . import views

app_name = "purchases"
urlpatterns = [
    path("<int:pk>/", views.PurchaseDetailView.as_view(), name="purchase"),
    path("select/", views.PurchaseSelectView.as_view(), name="select"),
    path("create_m/", views.CreateMaterialView.as_view(), name="create_m"),
    path("create_i/", views.CreateImmaterialView.as_view(), name="create_i"),
    path("material/<int:pk>/", views.MaterialDetailView.as_view(), name="material"),
    path(
        "immaterial/<int:pk>/", views.ImmaterialDetailView.as_view(), name="immaterial"
    ),
    path(
        "material/include/<int:pk>/", views.material_attend_view, name="material-attend"
    ),
    path(
        "material/delete/<int:pk>", views.material_delete_view, name="material-delete"
    ),
    path(
        "immaterial/include/<int:pk>/",
        views.immaterial_attend_view,
        name="immaterial-attend",
    ),
    path(
        "immaterial/delete/<int:pk>",
        views.immaterial_delete_view,
        name="immaterial-delete",
    ),
]
