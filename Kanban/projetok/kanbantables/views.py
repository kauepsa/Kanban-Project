from django.shortcuts import render, redirect, get_object_or_404
from .models import Projeto, Coluna, Item
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required 

def indexpage(request):
    return render(request, 'kanban/index.html')

@login_required(login_url='login')
def criar_projeto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        
        projeto = Projeto(nome=nome, descricao=descricao)
        projeto.save()
        projeto.managers.add(request.user)
        projeto.create_colunas_padrao()
        
        return redirect('index')
    
    return render(request, 'kanban/criar_projeto.html')

@login_required(login_url='login')
def lista_projetos(request):
    projetos = Projeto.objects.filter(Q(managers=request.user) | Q(users=request.user)).distinct()
    return render(request, 'kanban/lista_projetos.html', {'projetos': projetos})

@login_required(login_url='login')
def projeto_tables(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    is_manager = request.user in projeto.managers.all()
    is_participant = request.user in projeto.users.all()
    if not is_manager and not is_participant:
        return redirect('index')
    colunas = projeto.colunas.all()
    itens = []
    for coluna in colunas:
        itens.append(coluna.itens.all())
    return render(request, 'kanban/tables.html', {'projeto': projeto, 'colunas': colunas, 'itens': itens})


@login_required(login_url='index')
def criar_coluna(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    
    if not (request.user in projeto.managers.all() or request.user in projeto.users.all()):
        return redirect('index')

    if request.method == 'POST':
        coluna = Coluna(nome=request.POST.get('nome'), projeto=projeto, editavel=True)
        coluna.save()
        return redirect('visualizar_projeto', pk=projeto_id)

    return redirect('visualizar_projeto', pk=projeto_id)


@login_required(login_url='index')
def excluir_coluna(request, projeto_id, coluna_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    coluna = get_object_or_404(Coluna, pk=coluna_id, projeto=projeto)

    context = {
        'projeto' : projeto, 'coluna': coluna
    }

    if not request.user in projeto.managers.all():
        return redirect('index')

    if request.method == 'POST':
        coluna.delete()
        return redirect('visualizar_projeto', pk=projeto_id)

    return render(request, 'kanban/excluir_coluna.html', context)

@login_required(login_url='index')
def editar_coluna(request, projeto_id, coluna_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    coluna = get_object_or_404(Coluna, pk=coluna_id, projeto=projeto)

    context = {'projeto' : projeto,'coluna' : coluna}

    if not request.user in projeto.managers.all():
        return redirect('index')

    if request.method == 'POST':
        coluna.nome=request.POST.get('nome')
        coluna.save()
        return redirect('visualizar_projeto', pk=projeto_id)

    return render(request, 'kanban/editar_coluna.html', context)

@login_required(login_url='index')
def criar_item(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    coluna1 = request.POST.get('coluna')
    if not (request.user in projeto.managers.all() or request.user in projeto.users.all()):
        return redirect('index')
    
    if request.method == 'POST':
        item = Item(
            titulo=request.POST.get('titulo'),
            descricao=request.POST.get('descricao'),
            user=request.user,
            coluna=get_object_or_404(Coluna, id=coluna1)
            )
        item.save()
        return redirect('visualizar_projeto', pk=projeto_id)
    return redirect('visualizar_projeto', pk=projeto_id)
    

@login_required(login_url='index')
def excluir_item(request, projeto_id, coluna_id, item_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    coluna = get_object_or_404(Coluna, pk=coluna_id, projeto=projeto)
    item = get_object_or_404(Item, pk=item_id, coluna=coluna)
    context = {
        'projeto' : projeto,
        'coluna': coluna,
        'item' : item
    }

    if not (request.user in projeto.managers.all() or request.user in projeto.users.all()):
        return redirect('index')

    if request.method == 'POST':
        item.delete()
        return redirect('visualizar_projeto', pk=projeto_id)

    return render(request, 'kanban/excluir_item.html', context)