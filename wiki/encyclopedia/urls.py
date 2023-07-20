from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("save", views.save, name="save"),
    path("<str:title>", views.display, name="display"),
    path("<str:title>/edit", views.edit, name="edit")
]