from django.urls import path
from . import views

app_name = 'kanbantables'

urlpatterns = [
    path('', views.indexpage, name='index'),
    path('criar/', views.criar_projeto, name='criar_projeto'),
    path('listar/', views.lista_projetos, name='listar_projetos'),
    path('projeto/<int:pk>/', views.projeto_tables, name='visualizar_projeto'),
]
