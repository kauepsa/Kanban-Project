from django.urls import path
from .views import paginainicial, cadastroUsuario, loginUsuario, logoutUsuario, perfilUsuario, PerfilPublico
from django.views.generic import RedirectView
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('', views.paginainicial, name='index'),
    path('cadastro/', views.cadastroUsuario, name='cadastro'),
    path('login/', views.loginUsuario, name='login'),
    path('logout/', views.logoutUsuario, name='logout'),
    path('perfil/', views.perfilUsuario, name='perfil'),
    path('perfil/<str:username>/', views.PerfilPublico, name='perfil_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]