from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model


class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(help_text='<li>Digite um endereço de email válido.</li> <hr>', required=True, widget=forms.EmailInput(attrs={'class':'form-control text-left', 'placeholder':'email@mail.com ...','autocomplete':"off"}))
    nome = forms.CharField(required=True, label='Nome Completo', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nome...','autocomplete':"off"}))
    username = forms.CharField(required=True, label='Nome de Usuário', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Usuário...','autocomplete':"off"}))
    idade = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'rounded border form-control', 'min':'1', 'max':'150', 'placeholder':'0'}))
    password1 = forms.CharField(required=True ,label='Senha', widget=forms.PasswordInput(attrs={'class':'form-control border rounded', 'placeholder':'Senha...','autocomplete':"off"}), help_text='''
    <div class='card'>
    <div class='card-body bg-dark border rounded'>
    <h3 class="fs-5">Para ter uma senha segura , siga os seguintes critéritos:</h3>
    <ul>
    <li>Sua senha não deve possuir informações pessoais.</li>
    <li>Sua senha deve conter ao menos 8 caracteres.</li>
    <li>Não utilize a mesma senha para todos aplicativos.</li>
    <li>Sua senha não pode ser completamente numérica</li>
    </ul>
    </div>
    </div>
    ''')
    password2 = forms.CharField(required=True ,label='Confirmar Senha', help_text='<li>Digite a sua senha novamente.</li>', widget=forms.PasswordInput(attrs={'class':'form-control border rounded', 'placeholder':'Confirmar Senha...','autocomplete':"off"}))
    genero = forms.ChoiceField(required=True, label='Gênero', widget=forms.Select(attrs={'class':'form-select border rounded'}), choices=(('MASCULINO', 'Masculino'), ('FEMININO', 'Feminino'), ('OUTRO', 'Outro/Desejo não revelar')))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'nome', 'genero', 'idade', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CadastroUsuarioForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class LoginUsuarioForm(AuthenticationForm):
    def __ini__(self, *args, **kwargs):
        super(LoginUsuarioForm, self).__init__(self, *args, **kwargs)

    username = forms.CharField(
        widget=forms.TextInput(
        attrs={'class':'form-control mt-2 mb-2', 'placeholder':'Usuário ou Email ...', 'autocomplete':"off"}),
        label='Usuário ou Email')
    
    password = forms.CharField(
        required=True ,
        label='Senha', 
        widget=forms.PasswordInput(attrs={'class':'form-control mt-2 mb-2', 'placeholder':'Senha...','autocomplete':"off"}))
    

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False ,help_text='<li>Digite um endereço de email válido.</li> <hr>',widget=forms.EmailInput(attrs={'class':'form-control text-light text-left', 'placeholder':'email@mail.com ...','autocomplete':"off",'style':'background-color: rgba(0,0,0,0);'}))
    nome = forms.CharField(required=False, label='Nome Completo', widget=forms.TextInput(attrs={'class':'form-control text-light', 'placeholder':'Nome...','autocomplete':"off", 'style':'background-color: rgba(0,0,0,0);'}))
    genero = forms.ChoiceField(required=False, label='Gênero', widget=forms.Select(attrs={'class':'form-select bg-dark border text-light rounded'}), choices=(('MASCULINO', 'Masculino'), ('FEMININO', 'Feminino'), ('OUTRO', 'Outro/Desejo não revelar')))
    idade = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'rounded text-light border form-control', 'min':'1', 'max':'150', 'placeholder':'0', 'style':'background-color: rgba(0,0,0,0);'}))
    foto_perfil = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'type':'file', 'accept':'image/*', 'class':'sr-only', 'id':'foto-perfil-input'
    }))
    github = forms.URLField(required=False, label='Github', widget=forms.TextInput(attrs={'class':'form-control text-light', 'placeholder':'www.github.com/...','autocomplete':"off", 'style':'background-color: rgba(0,0,0,0);'}))
    linkedin = forms.URLField(required=False, label='Linkedin', widget=forms.TextInput(attrs={'class':'form-control text-light', 'placeholder':'www.linkedin.com/in/...','autocomplete':"off", 'style':'background-color: rgba(0,0,0,0);'}))
    descricao = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control text-light', 'placeholder':'Conte um pouco sobre você ...','autocomplete':"off", 'style':'background-color: rgba(0,0,0,0);', 'rows':'4'}))


    class Meta:
        model = get_user_model()
        fields = ['nome', 'email', 'genero', 'idade', 'foto_perfil', 'descricao' , 'linkedin', 'github']


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(required=True ,label='Nova Senha', widget=forms.PasswordInput(attrs={'class':'form-control border rounded', 'placeholder':'Senha...','autocomplete':"off"}), help_text='''
    <div class='card'>
    <div class='card-body bg-dark border rounded'>
    <h3 class="fs-5">Para ter uma senha segura , siga os seguintes critéritos:</h3>
    <ul>
    <li>Sua senha não deve possuir informações pessoais.</li>
    <li>Sua senha deve conter ao menos 8 caracteres.</li>
    <li>Não utilize a mesma senha para todos aplicativos.</li>
    <li>Sua senha não pode ser completamente numérica</li>
    </ul>
    </div>
    </div>
    ''')
    new_password2 = forms.CharField(required=True ,label='Confirmar Nova Senha', help_text='<li>Digite sua nova senha novamente.</li>', widget=forms.PasswordInput(attrs={'class':'form-control border rounded', 'placeholder':'Confirmar Senha...','autocomplete':"off"}))

    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    def __ini__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(self, *args, **kwargs)

    email = forms.EmailField(required=False ,help_text='',widget=forms.EmailInput(attrs={'class':'form-control text-left', 'placeholder':'email@mail.com ...','autocomplete':"off"}))