from django.urls import path
from .views import paginainicial, cadastroUsuario, loginUsuario, logoutUsuario, perfilUsuario
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.paginainicial, name='index'),
    path('cadastro/', views.cadastroUsuario, name='cadastro'),
    path('login/', views.loginUsuario, name='login'),
    path('logout/', views.logoutUsuario, name='logout'),
    path('perfil/', views.perfilUsuario, name='perfil')
]