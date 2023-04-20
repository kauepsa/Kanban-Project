from django.urls import path
from .views import paginainicial, cadastroUsuario, loginUsuario, logoutUsuario, perfilUsuario, PerfilPublico
from django.views.generic import RedirectView
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.paginainicial, name='index'),
    path('cadastro/', views.cadastroUsuario, name='cadastro'),
    path('login/', views.loginUsuario, name='login'),
    path('logout/', views.logoutUsuario, name='logout'),
    path('perfil/', views.perfilUsuario, name='perfil'),
    path('perfil/<str:username>/', views.PerfilPublico, name='perfil_detail'),
]