from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('inbox', views.inbox, name="inbox"),
    path('compose', views.compose, name="compose"),
]