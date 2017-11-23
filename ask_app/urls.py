from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^question/', views.question),
    url(r'^ask/', views.ask),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^params/', views.params)
]
