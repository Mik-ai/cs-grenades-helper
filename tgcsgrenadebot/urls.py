from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.UpdateBot.as_view(), name="update"),
]
