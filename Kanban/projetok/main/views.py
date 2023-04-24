from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Perfil
from django.contrib import messages
from django.http import Http404
from kanbantables.models import Projeto

def paginainicial(request):
    return render(request, 'main/index.html', {'user': request.user})


from django.core.files import File
from django.conf import settings
import os

from django.contrib.auth.models import Permission

def cadastroUsuario(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('index')
        else: 
            return render(request, 'main/cadastro.html')
    else:
        username = request.POST.get('username')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        idade = request.POST.get('idade')
        genero = request.POST.get('genero')
        user = User.objects.filter(username=username).first()
        if user and user.is_authenticated:
            return redirect('index')
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        
        permissions = Permission.objects.filter(content_type__app_label__startswith='admin')
        user.user_permissions.remove(*permissions)
        
        perfil = Perfil.objects.create(user=user, nome=nome, idade=idade, genero=genero)
        perfil.save()
        return redirect('index')


def loginUsuario(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('index')
        else: 
            return render(request, 'main/login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('Usuário ou senha incorreto!')
        

def logoutUsuario(request):
    logout(request)
    return redirect('index')


@login_required
def perfilUsuario(request):
    if request.method == "GET":
        perfil = Perfil.objects.get(user=request.user)
        context = {
            'perfil': perfil
        }
        return render(request, 'main/perfil.html', context)
    else:
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        genero = request.POST.get('genero')
        descricao = request.POST.get('descricao')
        linkedin = url_correct(request.POST.get('linkedin'))
        github = url_correct(request.POST.get('github'))
        foto_perfil = request.FILES.get('foto_perfil')
        foto_banner = request.FILES.get('foto_banner')

        perfil = Perfil.objects.get(user=request.user)
        perfil.nome = nome
        perfil.idade = idade
        perfil.genero = genero
        perfil.descricao = descricao
        perfil.linkedin = linkedin
        perfil.github = github

        if foto_perfil:
            if perfil.foto_perfil:
                perfil.foto_perfil.delete()
            perfil.foto_perfil = foto_perfil

        if foto_banner:
            if perfil.foto_banner:
                perfil.foto_banner.delete()
            perfil.foto_banner = foto_banner

        perfil.save()

        return redirect('perfil')



    
def PerfilPublico(request, username):
    try:
        perfil = Perfil.objects.get(user__username=username)
    except Perfil.DoesNotExist:
        messages.error(request, 'Usuário não existe')
        raise Http404('Usuário não existe')
    return render(request, 'main/teste.html', {'perfil': perfil})

def url_correct(url):
    if url.startswith("https://"):
        url = url[8:]
    if not url.startswith("www."):
        url = "www." + url
    return url


def search(request, search_field):
    projetos = Projeto.objects.filter(nome=search_field)
    usuarios = Perfil.objects.filter(user__username=search_field)

    context = {
        'projetos' : projetos,
        'usuarios' : usuarios,
        'search' : search_field
    }

    return render(request, 'main/search.html', context)