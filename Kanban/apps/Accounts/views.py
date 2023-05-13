from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CadastroUsuarioForm, LoginUsuarioForm, UserUpdateForm, SetPasswordForm, PasswordResetForm
from django.core.mail import send_mail
from django.contrib import messages
from .decorators import user_not_authenticated
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.db.models.query_utils import Q


@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = 'Solicitação de Recuperação de Senha - Projeto Kanban'
                message = render_to_string("accounts/nologin_password_reset.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    'protocol': 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request, f'Foi enviado um email com a Solicitação de Recuperação de Senha para <strong>{associated_user.email}</strong> ,  por favor verifique seu inbox ou sua caixa de SPAM para recuperar sua senha!')
                else:
                    messages.error(request, 'Ops , parece que aconteceu algum erro durante o envio do email, por favor tente novamente mais tarde.')
            return redirect('index')

    form = PasswordResetForm()
    return render(
        request=request,
        template_name='accounts/password_reset.html',
        context={'form':form}
    )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Senha trocada com sucesso! Por favor faça o login com a sua nova senha.')
                return redirect('index')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})

    else:
        messages.error(request, 'Link de recuperação de senha inválido ou expirado!')

    messages.error(request, 'Algum imprevisto aconteceu , estamos te redirecionando para a página principal.')
    return redirect('index')



@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('index')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'accounts/password_reset_confirm.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Obrigado por confirmar seu email , agora você já pode logar na sua conta e utilizar livremente nossa plataforma!')
    else:
        return redirect('index')
    return redirect('index')

def ativarEmail(request, user, to_mail):
    mail_subject = 'Verificação de E-mail Projeto Kanban'
    message = render_to_string("accounts/email_verification.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_mail])
    if email.send():
        messages.success(request, f'Cadastro efetuado com sucesso. Bem-vindo , <strong>{user}</strong>!<br> Um email de verificação será enviado para <strong>{to_mail}</strong> , por favor verifique seu inbox ou sua caixa de SPAM para finalizar a etapa de verificação de email!')
    else:
        messages.error(request, f'Parece que ocorreu um erro ao enviar um email para <strong>{to_mail}</strong>, verifique se você digitou um email válido ou se digitou corretamente o email!')


@user_not_authenticated
def cadastro(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            ativarEmail(request, user, form.cleaned_data.get('email'))

            return redirect('index')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = CadastroUsuarioForm()
    return render(
        request=request,
        template_name='accounts/registro.html',
        context={'form': form}
    )

@user_not_authenticated
def login_view(request):
    if request.method == 'POST':
        form = LoginUsuarioForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)

                messages.success(request, f'Ola <strong>{user.username}</strong>, Bem-vindo(a)!')
                return redirect('index')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = LoginUsuarioForm()
    return render(
        request=request,
        template_name="accounts/login.html",
        context={"form":form}
        )


@login_required(login_url='login')
def logout_view(request):
    messages.info(request, 'Deslogado com sucesso!')
    logout(request)
    return redirect('index')




def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, 'Alterações salvas com sucesso!')
            return redirect('perfil', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(
            request=request,
            template_name='accounts/perfil.html',
            context={'form': form}
        )
    return redirect('index')
