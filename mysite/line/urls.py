from django.urls import path

from . import views

app_name = "line"
urlpatterns = [
    path("", views.index, name="index"),
]