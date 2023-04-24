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
        
        return redirect('listar_projetos')
    
    return render(request, 'kanban/criar_projeto.html')

@login_required(login_url='index')
def editar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    context = {
        'projeto' : projeto
    }

    if not request.user in projeto.managers.all():
        return redirect('index')
    
    if request.method == 'POST':
        projeto.nome = request.POST.get('nome')
        projeto.descricao = request.POST.get('descricao')
        projeto.save()
        return redirect('visualizar_projeto', projeto_id)
    return render(request, 'kanban/editar_projeto.html', context)

@login_required(login_url='index')
def excluir_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)

    context = {
        'projeto' : projeto
    }

    if not request.user in projeto.managers.all():
        return redirect('index')

    if request.method == 'POST':
        projeto.delete()
        return redirect('index')
    
    return render(request, 'kanban/excluir_projeto.html', context)


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
    
    if not request.user in projeto.managers.all():
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


@login_required(login_url='index')
def editar_item(request, projeto_id, item_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    colunas = Coluna.objects.filter(projeto_id=projeto)
    item = get_object_or_404(Item, pk=item_id)

    context = {
        'projeto' : projeto,
        'colunas' : colunas,
        'item' : item
    }
    

    if not (request.user in projeto.managers.all() or request.user in projeto.users.all()):
        return redirect('index')
    
    if request.method == 'POST':
        item.titulo = request.POST.get('titulo')
        item.descricao = request.POST.get('descricao')
        item.coluna = get_object_or_404(Coluna, id=request.POST.get('coluna'))
        item.save()
        return redirect('visualizar_projeto', pk=projeto_id)
    
    return render(request, 'kanban/editar_item.html', context)


@login_required(login_url='index')
def gerenciar_membros(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)

    context = {
        'projeto' : projeto
    }

    if not request.user in projeto.managers.all():
        return redirect('index')
    
    return render(request, 'kanban/gerenciar_membros.html', context)

def adicionar_manager(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    manager = request.POST.get('manager')

    if not request.user in projeto.managers.all():
        return redirect('index')

    if request.method == 'POST':
        projeto.managers.add(manager)
        projeto.users.remove(manager)
        projeto.save()
    
    return redirect('gerenciar_membros', projeto_id)

def adicionar_membro(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    membro = get_object_or_404(User, username=request.POST.get('membro'))

    if not request.user in projeto.managers.all():
        return redirect('index')

    if request.method == 'POST':
        if membro not in projeto.managers.all():
            projeto.convidados.add(membro)
        projeto.save()
    
    return redirect('gerenciar_membros', projeto_id)

def cancelar_convite(request, projeto_id, convite_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)

    if not request.user in projeto.managers.all():
        return redirect('index')
    
    if request.user in projeto.managers.all():
        projeto.convidados.remove(convite_id)
        projeto.save()

    return redirect('gerenciar_membros', projeto_id)

        
def grupo_request(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)

    if (request.user in projeto.managers.all() or request.user in projeto.users.all()):
        return redirect('vizualizar_projeto', projeto_id)
    else:
        projeto.pendentes.add(request.user)
        projeto.save()
        return redirect('listar_projetos')
    

def cancelar_pendente(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    projeto.pendentes.remove(request.user)
    projeto.save()
    return redirect('listar_projetos')


def recusar_convite(request, projeto_id, solicitacao_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    
    if (request.user in projeto.managers.all() or request.user in projeto.users.all()):
        projeto.pendentes.remove(solicitacao_id)
        projeto.save()
        return redirect('listar_projetos')

def aceitar_convite(request, projeto_id, solicitacao_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)

    if (request.user in projeto.managers.all() or request.user in projeto.users.all()):
        projeto.pendentes.remove(solicitacao_id)
        projeto.users.add(solicitacao_id)
        return redirect('listar_projetos')

    
    