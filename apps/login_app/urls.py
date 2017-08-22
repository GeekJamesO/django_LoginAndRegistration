from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^home$', views.home),
    # url(r'^new$', views.new),
    # url(r'^create$', views.create),  # Post method sends here..
    # url(r'^(?P<number>\d+)$', views.show),
    # url(r'^(?P<number>\d+)/edit$', views.edit),
    # url(r'^(?P<number>\d+)/delete$', views.destroy),
]
