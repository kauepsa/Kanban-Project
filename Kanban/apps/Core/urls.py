from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('suporte', views.suporte, name='suporte'),
    path('sobre', views.sobre, name='sobre'),
]