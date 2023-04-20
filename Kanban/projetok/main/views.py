from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Perfil

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
        linkedin = request.POST.get('linkedin')
        github = request.POST.get('github')

        perfil = Perfil.objects.update(
            nome=nome, idade=idade, genero=genero, descricao=descricao,
            linkedin=linkedin, github=github 
            )
        return redirect('perfil')