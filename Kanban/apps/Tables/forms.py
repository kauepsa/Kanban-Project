from django.contrib.auth import get_user_model
from django import forms
from .models import Projeto, Coluna, Item
User = get_user_model()

class ProjetoForm(forms.ModelForm):

    class Meta:
        model = Projeto
        fields = ['titulo', 'descricao', 'prazo', 'publico']

        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control text-light', 'placeholder':'Título ou nome do projeto ...','autocomplete':"off", 'style':'background-color: rgba(0,0,0,0);'}),
            'descricao': forms.Textarea(attrs={'class':'form-control text-light', 'placeholder':'Fale um pouco sobre o projeto ...','autocomplete':"off", 'rows':'4', 'style':'background-color: rgba(0,0,0,0);'}),
            'prazo': forms.DateTimeInput(attrs={'class':'form-control text-light' ,'autocomplete':"off", 'type': 'datetime-local', 'style':'background-color: rgba(0,0,0,0);'}),
            'publico': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ColunaForm(forms.ModelForm):
    class Meta:
        model = Coluna
        fields = ['nome']