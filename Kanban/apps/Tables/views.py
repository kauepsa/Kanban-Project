from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Projeto, Coluna, Item
from .forms import ProjetoForm
from django.urls import reverse_lazy
from django.db.models import Count, Q
from apps.Accounts.models import Profile

##################- Controle de Entradas e Saídas -###############################

class GerenciarMembros(LoginRequiredMixin, View):
    template_name = 'tables/gerenciar_membros.html'

    def get(self, request, *args, **kwargs):
        try:
            projeto = Projeto.objects.get(pk=kwargs['pk'])
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado.')
            return redirect('index')

        return render(request, self.template_name, {'projeto': projeto})


@login_required
def transferir_dono(request, projeto_id, user_id):
    if request.method == 'POST':
        try:
            projeto = Projeto.objects.get(pk=projeto_id)
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado/inválido.')
            return redirect('index')

        if request.user == projeto.dono:
            try:
                novo_dono = Profile.objects.get(pk=user_id)
            except Profile.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
                return redirect('index')

            projeto.dono = novo_dono # Atribui o novo usuário como o novo dono do projeto
            projeto.save() # Salva as alterações no objeto projeto

            # Adiciona o usuário anterior como moderador do projeto
            projeto.moderadores.add(request.user)
            projeto.moderadores.remove(novo_dono)

            messages.success(request, 'O dono do projeto foi transferido com sucesso.')
            return redirect('lista_projetos')

    messages.error(request, 'Você não tem permissão para transferir o dono do projeto.')
    return redirect('index')



@login_required
def adicionar_moderador(request, projeto_id, user_id):
    if request.method == 'POST':
        try:
            projeto = Projeto.objects.get(pk=projeto_id)
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado/inválido.')
            return redirect('index')

        if request.user == projeto.dono:
            try:
                user = Profile.objects.get(pk=user_id)
            except Profile.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
                return redirect('index')


            projeto.moderadores.add(user)
            projeto.membros.remove(user)
            projeto.save()
            messages.success(request, f'<strong>{user}</strong> se tornou um moderador!')
            return redirect('gerenciar_membros', projeto.id)
        else:
            messages.error(request, 'Você não tem permissão para executar esta ação.')
            return redirect('projeto_detail', projeto.id)
    else:
        messages.error(request, 'Você não tem permissão para acessar este URL.')
        return redirect('index')

@login_required
def remover_moderador(request, projeto_id, user_id):
    if request.method == 'POST':
        try:
            projeto = Projeto.objects.get(pk=projeto_id)
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado/inválido.')
            return redirect('index')

        if request.user == projeto.dono:
            try:
                user = Profile.objects.get(pk=user_id)
            except Profile.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
                return redirect('index')

            projeto.moderadores.remove(user)
            projeto.membros.add(user)
            projeto.save()
            messages.success(request, f'<strong>{user}</strong> deixou de ser um moderador!')
            return redirect('gerenciar_membros', projeto.id)
        else:
            messages.error(request, 'Você não tem permissão para executar esta ação.')
            return redirect('projeto_detail', projeto.id)
    else:
        messages.error(request, 'Você não tem permissão para acessar este URL.')
        return redirect('index')


@login_required
def remover_membro(request, projeto_id, user_id):
    if request.method == 'POST':
        try:
            projeto = Projeto.objects.get(pk=projeto_id)
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado/inválido.')
            return redirect('index')

        if request.user == projeto.dono or request.user in projeto.moderadores.all():
            try:
                user = Profile.objects.get(pk=user_id)
            except Profile.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
                return redirect('index')


            if user in projeto.membros:
                projeto.membros.remove(user)
                projeto.save()
                messages.success(request, f'<strong>{user}</strong> foi removido do projeto!')
                return redirect('gerenciar_membros', projeto.id)
        else:
            messages.error(request, 'Você não tem permissão para executar esta ação.')
            return redirect('projeto_detail', projeto.id)
    else:
        messages.error(request, 'Você não tem permissão para acessar este URL.')
        return redirect('index')

@login_required
def convidar_membro(request, projeto_id):
    if request.method == 'POST':
        try:
            projeto = Projeto.objects.get(pk=projeto_id)
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado/inválido.')
            return redirect('index')

        if request.user == projeto.dono or request.user in projeto.moderadores.all():
            try:
                user = Profile.objects.get(username=request.POST.get('membro'))
            except Profile.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
                return redirect('gerenciar_membros', projeto.id)


            if user not in projeto.moderadores.all() and user not in projeto.membros.all() and user != projeto.dono:
                projeto.convites_enviados.add(user)
                projeto.save()
                messages.success(request, f'Um convite foi enviado para <strong>{user}</strong>!')
                return redirect('gerenciar_membros', projeto.id)
            else:
                messages.error(request, 'Este usuário já faz parte do projeto/grupo!')
                return redirect('gerenciar_membros', projeto.id)
        else:
            messages.error(request, 'Você não tem permissão para executar esta ação.')
            return redirect('projeto_detail', projeto.id)
    else:
        messages.error(request, 'Você não tem permissão para acessar este URL.')
        return redirect('index')

@login_required
def cancelar_convite(request, projeto_id, invite_id):
    if request.method == 'POST':
        try:
            projeto = Projeto.objects.get(pk=projeto_id)
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado/inválido.')
            return redirect('index')

        if request.user == projeto.dono or request.user in projeto.moderadores.all():
            try:
                user = Profile.objects.get(pk=invite_id)
            except Profile.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
                return redirect('index')

            if user not in projeto.moderadores.all() and user not in projeto.membros.all() and user != projeto.dono:
                projeto.convites_enviados.remove(user)
                projeto.save()
                messages.success(request, f'O convite para <strong>{user}</strong> foi cancelado!')
                return redirect('gerenciar_membros', projeto.id)
        else:
            messages.error(request, 'Você não tem permissão para executar esta ação.')
            return redirect('projeto_detail', projeto.id)
    else:
        messages.error(request, 'Você não tem permissão para acessar este URL.')
        return redirect('index')

@login_required
def aceitar_solicitacao(request, projeto_id, invite_id):
    if request.method == 'POST':
        try:
            projeto = Projeto.objects.get(pk=projeto_id)
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado/inválido.')
            return redirect('index')

        if request.user == projeto.dono or request.user in projeto.moderadores.all():
            try:
                user = Profile.objects.get(pk=invite_id)
            except Profile.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
                return redirect('index')

            if user not in projeto.moderadores.all() and user not in projeto.membros.all() and user != projeto.dono:
                projeto.membros.add(user)
                projeto.solicitacoes_entrada.remove(user)
                projeto.save()
                messages.success(request, f'<strong>{user}</strong> se tornou um integrante do projeto!')
                return redirect('gerenciar_membros', projeto.id)
        else:
            messages.error(request, 'Você não tem permissão para executar esta ação.')
            return redirect('projeto_detail', projeto.id)
    else:
        messages.error(request, 'Você não tem permissão para acessar este URL.')
        return redirect('index')

@login_required
def recusar_solicitacao(request, projeto_id, invite_id):
    if request.method == 'POST':
        try:
            projeto = Projeto.objects.get(pk=projeto_id)
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado/inválido.')
            return redirect('index')

        if request.user == projeto.dono or request.user in projeto.moderadores.all():
            user = Profile.objects.get(pk=invite_id)
            if user not in projeto.moderadores.all() and user not in projeto.membros.all() and user != projeto.dono:
                projeto.solicitacoes_entrada.remove(user)
                projeto.save()
                messages.success(request, f'Você recusou a solicitação de entrada de <strong>{user}</strong>!')
                return redirect('gerenciar_membros', projeto.id)
        else:
            messages.error(request, 'Você não tem permissão para executar esta ação.')
            return redirect('projeto_detail', projeto.id)
    else:
        messages.error(request, 'Você não tem permissão para acessar este URL.')
        return redirect('index')

@login_required
def aceitar_convite(request, projeto_id):
    if request.method == "POST":
        try:
            projeto = Projeto.objects.get(pk=projeto_id)
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado/inválido.')
            return redirect('index')

        user = request.user
        if user not in projeto.moderadores.all() and user not in projeto.membros.all() and user != projeto.dono:
            projeto.convites_enviados.remove(user)
            projeto.membros.add(user)
            projeto.save()
            messages.success(request, f'Você aceitou o convite de <strong>{projeto.titulo}<strong> , agora você faz parte da equipe do projeto!')
            return redirect('projeto_detail', projeto.id)
        else:
            messages.error(request, 'Você já faz parte desse grupo.')
            return redirect('projeto_detail', projeto.id)
    else:
        messages.error(request, 'Você não tem permissão para acessar este URL.')
        return redirect('index')


@login_required
def recusar_convite(request, projeto_id):
    if request.method == "POST":
        try:
            projeto = Projeto.objects.get(pk=projeto_id)
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado/inválido.')
            return redirect('index')

        user = request.user
        if user not in projeto.moderadores.all() and user not in projeto.membros.all() and user != projeto.dono:
            projeto.convites_enviados.remove(user)
            projeto.save()
            messages.success(request, f'Você recusou o convite de <strong>{projeto.titulo}<strong>!')
            return redirect('projeto_detail', projeto.id)
        else:
            messages.error(request, 'Você já faz parte desse grupo.')
            return redirect('projeto_detail', projeto.id)
    else:
        messages.error(request, 'Você não tem permissão para acessar este URL.')
        return redirect('index')


@login_required
def solicitar_entrada(request, projeto_id):
    if request.method == "POST":
        try:
            projeto = Projeto.objects.get(pk=projeto_id)
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado/inválido.')
            return redirect('index')

        user = request.user
        if user not in projeto.moderadores.all() and user not in projeto.membros.all() and user != projeto.dono:
            projeto.solicitacoes_entrada.add(user)
            projeto.save()
            messages.success(request, f'Você enviou uma solicitação de entrada para <strong>{projeto.titulo}</strong> , agora basta aguardar a resposta da moderação!')
            return redirect('projeto_detail', projeto.id)
        else:
            messages.error(request, 'Você já faz parte desse grupo.')
            return redirect('projeto_detail', projeto.id)
    else:
        messages.error(request, 'Você não tem permissão para acessar este URL.')
        return redirect('index')

@login_required
def cancelar_entrada(request, projeto_id):
    if request.method == "POST":
        try:
            projeto = Projeto.objects.get(pk=projeto_id)
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado/inválido.')
            return redirect('index')

        user = request.user
        if user in projeto.solicitacoes_entrada.all():
            projeto.solicitacoes_entrada.remove(user)
            projeto.save()
            messages.success(request, f'Você cancelou a solicitação de entrada para <strong>{projeto.titulo}</strong>!')
            return redirect('projeto_detail', projeto.id)
        else:
            messages.error(request, 'Você já faz cancelou esta solicitação.')
            return redirect('projeto_detail', projeto.id)
    else:
        messages.error(request, 'Você não tem permissão para acessar este URL.')
        return redirect('index')


#######################- Views relacionadas diretamente aos projetos -###############################

def search(request, search_field):
    try:
        projetos = Projeto.objects.filter(titulo=search_field)
    except Projeto.DoesNotExist:
        messages.error(request, 'Não há nenhum projeto com este Nome ou Título , verifique se você digitou corretamente .')
        return redirect('index')

    context = {
        'projetos' : projetos,
        'search' : search_field
    }

    return render(request, 'tables/search_projetos.html', context)


class ProjetoDetailView(LoginRequiredMixin, View):
    template_name = 'tables/painel_projeto.html'

    def get(self, request, *args, **kwargs):
        try:
            projeto = Projeto.objects.get(pk=kwargs['pk'])
        except Projeto.DoesNotExist:
            messages.error(request, 'Projeto não encontrado.')
            return redirect('index')

        return render(request, self.template_name, {'projeto': projeto})



class ProjetoSairView(View):
    def get(self, request, *args, **kwargs):
        try:
            projeto = Projeto.objects.get(pk=kwargs['pk'])
        except Projeto.DoesNotExist:
            messages.error(request, 'O projeto não existe.')
            return redirect('lista_projetos')

        user = request.user

        if user == projeto.dono:
            if projeto.moderadores.exists() or projeto.membros.exists():
                messages.error(request,
                'Para sair do projeto você deve transferir o lider para algum moderador , ou expulsar todos os membros e moderadores do projeto!')
                return redirect('projeto_detail', projeto.id)
            else:
                projeto.delete()
        else:
            projeto.moderadores.remove(user)
            projeto.membros.remove(user)

        return redirect('lista_projetos')

class ListaProjetosView(LoginRequiredMixin, ListView):
    template_name = 'tables/lista_projetos.html'
    context_object_name = 'projetos'

    def get_queryset(self):
        usuario = self.request.user
        projetos_pertencentes = Projeto.objects.filter(
            Q(dono=usuario) | Q(moderadores=usuario) | Q(membros=usuario)
        )
        projetos_top10 = Projeto.objects.annotate(
            num_membros=Count('membros') + Count('moderadores') + 1
        ).order_by('-num_membros', '-criado_em')[:10]
        convites = Projeto.objects.filter(convites_enviados=self.request.user).distinct()
        projetos = {
            'projetos_pertencentes':projetos_pertencentes,
            'projetos_top10':projetos_top10,
            'convites':convites
        }
        return projetos



class ProjetoCreateView(LoginRequiredMixin, CreateView):
    model = Projeto
    form_class = ProjetoForm
    template_name = 'tables/criar_projeto.html'
    success_url = reverse_lazy('index')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.dono = self.request.user
        self.object.save()

        return super().form_valid(form)

class ProjetoEditarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Projeto
    template_name = 'tables/editar_projeto.html'
    form_class = ProjetoForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        projeto = self.get_object()
        if self.request.user == projeto.dono:
            return super().form_valid(form)
        else:
            return redirect('lista_projetos')

    def test_func(self):
        projeto = self.get_object()
        return self.request.user == projeto.dono


##########################- Views CRUD de Colunas -#############################


@login_required(login_url='index')
def tables(request, projeto_id):
    if request.method == 'GET':

        projeto = Projeto.objects.get(pk=projeto_id)
        colunas = Coluna.objects.filter(projeto=projeto)
        itens = Item.objects.filter(coluna__in=colunas)
        context = {
            'projeto':projeto,
            'colunas':colunas,
            'itens':itens
        }
        user = request.user
        if user in projeto.moderadores.all() or user in projeto.membros.all() or user == projeto.dono:
            return render(request, 'tables/tables.html', context)
        else:
            messages.error(request, 'Você não tem permissão para acessar este link! <br> (Você não faz parte deste grupo)')
            return redirect('index')
    else:
        return redirect('index')


@login_required(login_url='index')
def tarefas(request, projeto_id):
    projeto = Projeto.objects.get(pk=projeto_id)
    user = request.user

    if user in projeto.moderadores.all() or user in projeto.membros.all() or user == projeto.dono:
        tarefas = Item.objects.filter(projeto=projeto, criado_por=user)
        context = {
            'tarefas': tarefas,
            'projeto': projeto
            }
        return render(request, 'tables/tarefas.html', context)
    else:
        messages.error(request, 'Você não tem permissão para acessar este link! <br> (Você não faz parte deste grupo)')
        return redirect('index')


@login_required(login_url='index')
def criar_coluna(request, projeto_id):
    projeto = Projeto.objects.get(pk=projeto_id)
    if request.user == projeto.dono or request.user in projeto.moderadores.all():
        if request.method == 'POST':

                coluna = Coluna(nome=request.POST.get('nome'), projeto=projeto, editavel=True)
                coluna.save()
                return redirect('tables', projeto_id)
    else:
        messages.error(request, 'Você não tem permissão para isso ...')
        return redirect('tables', projeto_id)

    return redirect('tables', projeto_id)

@login_required(login_url='index')
def excluir_coluna(request, projeto_id, coluna_id):
    projeto = Projeto.objects.get(pk=projeto_id)
    coluna = Coluna.objects.get(pk=coluna_id, projeto=projeto)

    context = {
        'projeto' : projeto, 'coluna': coluna
    }

    if request.method == 'POST':
        if request.user == projeto.dono or request.user in projeto.moderadores.all():
            coluna.delete()
            return redirect('tables', projeto_id)

    if request.method == 'GET':
        if request.user in projeto.moderadores.all() or request.user == projeto.dono:
            return render(request, 'tables/excluir_coluna.html', context)
        else:
            messages.error(request, 'Você não tem permissão para isso ...')
            return redirect('tables', projeto_id)



@login_required(login_url='index')
def editar_coluna(request, projeto_id, coluna_id):

    projeto = Projeto.objects.get(pk=projeto_id)
    coluna = Coluna.objects.get(pk=coluna_id, projeto=projeto)
    context = {'projeto' : projeto,'coluna' : coluna}

    if request.method == 'POST':
            coluna.nome=request.POST.get('nome')
            coluna.save()
            return redirect('tables', projeto_id)

    if request.method == 'GET':
        if request.user in projeto.moderadores.all() or request.user == projeto.dono:
            return render(request, 'tables/editar_coluna.html', context)
        else:
            messages.error(request, 'Você não tem permissão para isso ...')
            return redirect('tables', projeto_id)




@login_required(login_url='index')
def criar_item(request, projeto_id):
    projeto = Projeto.objects.get(pk=projeto_id)
    coluna1 = request.POST.get('coluna')
    if not (request.user in projeto.moderadores.all() or request.user in projeto.membros.all() or request.user == projeto.dono):
        messages.error(request, 'Você não faz parte deste grupo!')
        return redirect('index')

    if request.method == 'POST':
        item = Item(
            titulo=request.POST.get('titulo'),
            descricao=request.POST.get('descricao'),
            criado_por=request.user,
            coluna=Coluna.objects.get(id=coluna1),
            projeto=projeto
            )
        item.save()
        return redirect('tables', projeto_id)
    return redirect('tables', projeto_id)


@login_required(login_url='index')
def editar_item(request, projeto_id, item_id):
    projeto = Projeto.objects.get(pk=projeto_id)
    colunas = Coluna.objects.filter(projeto_id=projeto)
    item = Item.objects.get(pk=item_id)

    context = {
        'projeto' : projeto,
        'colunas' : colunas,
        'item' : item
    }


    if not (request.user in projeto.moderadores.all() or request.user in projeto.membros.all() or request.user == projeto.dono):
        return redirect('index')

    if request.method == 'POST':
        item.titulo = request.POST.get('titulo')
        item.descricao = request.POST.get('descricao')
        item.coluna = Coluna.objects.get(id=request.POST.get('coluna'))
        item.save()
        return redirect('tables', projeto_id)

    return render(request, 'tables/editar_item.html', context)

@login_required(login_url='index')
def excluir_item(request, projeto_id, coluna_id, item_id):
    projeto = Projeto.objects.get(pk=projeto_id)
    coluna = Coluna.objects.get(pk=coluna_id, projeto=projeto)
    item = Item.objects.get(pk=item_id, coluna=coluna)
    context = {
        'projeto' : projeto,
        'coluna': coluna,
        'item' : item
    }

    if not (request.user in projeto.moderadores.all() or request.user in projeto.membros.all() or request.user == projeto.dono):
        return redirect('index')

    if request.method == 'POST':
        item.delete()
        return redirect('tables', projeto_id)

    return render(request, 'tables/excluir_item.html', context)
