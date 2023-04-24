from django.urls import path
from .views import paginainicial, cadastroUsuario, loginUsuario, logoutUsuario, perfilUsuario, PerfilPublico, search
from . import views
import kanbantables.views as tables
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
    path('search/<str:search_field>', views.search, name='search'),

    path('projeto/listar', tables.lista_projetos, name='listar_projetos'),
    path('projeto/criar', tables.criar_projeto, name='criar_projeto'),
    path('projeto/excluir/<int:projeto_id>', tables.excluir_projeto, name='excluir_projeto'),

    path('projeto/editar/<int:projeto_id>', tables.editar_projeto, name='editar_projeto'),
    path('projeto/<int:pk>/', tables.projeto_tables, name='visualizar_projeto'),

    path('projeto/criar_coluna/<int:projeto_id>/', tables.criar_coluna, name='criar_coluna'),
    path('projeto/<int:projeto_id>/excluir_coluna/<int:coluna_id>/', tables.excluir_coluna, name='excluir_coluna'),
    path('projeto/<int:projeto_id>/editar_coluna/<int:coluna_id>/', tables.editar_coluna, name='editar_coluna'),

    path('projeto/criar_item/<int:projeto_id>/', tables.criar_item, name='criar_item'),
    path('projeto/<int:projeto_id>/excluir_item/<int:coluna_id>/<int:item_id>', tables.excluir_item, name='excluir_item'),
    path('projeto/<int:projeto_id>/editar_item/<int:item_id>/', tables.editar_item, name='editar_item'),

    path('projeto/<int:projeto_id>/gerenciar_membros/', tables.gerenciar_membros, name='gerenciar_membros'),
    path('projeto/<int:projeto_id>/adicionar_manager/', tables.adicionar_manager, name='adicionar_manager'),
    path('projeto/<int:projeto_id>/adicionar_membro/', tables.adicionar_membro, name='adicionar_membro'),
    path('projeto/<int:projeto_id>/convite/<int:convite_id>/', tables.cancelar_convite, name='cancelar_convite'),
    path('projeto/<int:projeto_id>/solicitacao/', tables.grupo_request, name='solicitar_entrada'),
    path('projeto/<int:projeto_id>/cancelar_solicitacao/', tables.cancelar_pendente, name='cancelar_solicitacao'),

    path('projeto/<int:projeto_id>/cancelar_solicitacao/<int:solicitacao_id>/', tables.recusar_convite, name='recusar_solicitacao'),
    path('projeto/<int:projeto_id>/aceitar_solicitacao/<int:solicitacao_id>/', tables.aceitar_convite, name='aceitar_solicitacao'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]