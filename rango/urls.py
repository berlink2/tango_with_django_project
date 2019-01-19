from django.conf.urls import url
from rango import views
from django.conf.urls import include

urlpatterns = [

    url(r'^$', views.index, name ='index'),


]