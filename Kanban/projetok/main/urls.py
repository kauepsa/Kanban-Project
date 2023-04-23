from django.urls import path
from .views import paginainicial, cadastroUsuario, loginUsuario, logoutUsuario, perfilUsuario, PerfilPublico
from . import views
from kanbantables.views import (
    lista_projetos, criar_projeto, projeto_tables, criar_coluna, excluir_coluna, 
    criar_item, excluir_item, editar_coluna
    )
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('', views.paginainicial, name='index'),
    path('cadastro/', views.cadastroUsuario, name='cadastro'),
    path('projeto/listar', lista_projetos, name='listar_projetos'),
    path('projeto/criar', criar_projeto, name='criar_projeto'),
    path('projeto/<int:pk>/', projeto_tables, name='visualizar_projeto'),
    path('projeto/criar_coluna/<int:projeto_id>/', criar_coluna, name='criar_coluna'),
    path('projeto/criar_item/<int:projeto_id>/', criar_item, name='criar_item'),
    path('projeto/<int:projeto_id>/excluir_coluna/<int:coluna_id>/', excluir_coluna, name='excluir_coluna'),
    path('projeto/<int:projeto_id>/excluir_item/<int:coluna_id>/<int:item_id>', excluir_item, name='excluir_item'),
    path('projeto/<int:projeto_id>/editar_coluna/<int:coluna_id>/', editar_coluna, name='editar_coluna'),
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