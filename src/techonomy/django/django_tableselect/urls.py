from django.urls import path

from . import views

app_name = "django_tableselect"

urlpatterns = [
    path("", views.index, name="index"),
]
