from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/status/", views.status, name="status"),
]
