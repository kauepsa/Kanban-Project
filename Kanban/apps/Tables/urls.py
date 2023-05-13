from django.urls import path
from . import views

urlpatterns = [
    path('lista_projetos/', views.ListaProjetosView.as_view(), name='lista_projetos'),
    path('criar_projeto/', views.ProjetoCreateView.as_view(), name='criar_projeto'),
    path('<int:pk>/editar', views.ProjetoEditarView.as_view(), name='editar_projeto'),
    path('<int:pk>/sair/', views.ProjetoSairView.as_view(), name='projeto_sair'),
    path('<int:projeto_id>/transferir-dono/<int:user_id>/', views.transferir_dono, name='transferir_dono'),
    path('<int:pk>/', views.ProjetoDetailView.as_view(), name='projeto_detail'),
    path('search/<str:search_field>', views.search, name='search'),
    path('<int:pk>/gerenciar-membros/', views.GerenciarMembros.as_view(), name='gerenciar_membros'),
    path('<int:projeto_id>/gerenciar-membros/adicionar-moderador/<int:user_id>/', views.adicionar_moderador, name='adicionar_moderador'),
    path('<int:projeto_id>/gerenciar-membros/remover-moderador/<int:user_id>/', views.remover_moderador, name='remover_moderador'),
    path('<int:projeto_id>/gerenciar-membros/remover-membro/<int:user_id>/', views.remover_membro, name='remover_membro'),
    path('<int:projeto_id>/gerenciar-membros/convidar-membro/', views.convidar_membro, name='convidar_membro'),
    path('<int:projeto_id>/gerenciar-membros/cancelar-convite/<int:invite_id>/', views.cancelar_convite, name='cancelar_convite'),
    path('<int:projeto_id>/gerenciar-membros/aceitar-solicitacao/<int:invite_id>/', views.aceitar_solicitacao, name='aceitar_solicitacao'),
    path('<int:projeto_id>/gerenciar-membros/recusar-solicitacao/<int:invite_id>/', views.recusar_solicitacao, name='recusar_solicitacao'),
    path('<int:projeto_id>/solicitar-entrada/', views.solicitar_entrada, name='solicitar_entrada'),
    path('<int:projeto_id>/cancelar-entrada/', views.cancelar_entrada, name='cancelar_entrada'),
    path('<int:projeto_id>/aceitar-convite/', views.aceitar_convite, name='aceitar_convite'),
    path('<int:projeto_id>/recusar-convite/', views.recusar_convite, name='recusar_convite'),
    path('<int:projeto_id>/tables', views.tables, name='tables'),
    path('<int:projeto_id>/tables/tarefas/', views.tarefas, name='tarefas'),
    path('<int:projeto_id>/tables/criar-coluna', views.criar_coluna, name='criar_coluna'),
    path('<int:projeto_id>/tables/excluir-coluna/<int:coluna_id>', views.excluir_coluna, name='excluir_coluna'),
    path('<int:projeto_id>/tables/editar-coluna/<int:coluna_id>', views.editar_coluna, name='editar_coluna'),
    path('<int:projeto_id>/tables/criar-item', views.criar_item, name='criar_item'),
    path('<int:projeto_id>/tables/editar-item/<int:item_id>', views.editar_item, name='editar_item'),
    path('<int:projeto_id>/tables/excluir-item/<int:coluna_id>/<int:item_id>', views.excluir_item, name='excluir_item'),
]

