from collections.abc import Mapping
from typing import Any
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Nome'}), 
        required=True, 
        label='')
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Senha'}), 
        required=True,
        label='')
    
    def clean_username(self):
        return self.cleaned_data.get('username').strip().title()

    def clean(self):
        super(LoginForm, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError('Usuário ou senha invalido')


class CadastrarForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Nome'}), 
        required=True, 
        label='')
    
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Senha'}), 
        required=True,
        label='')
    
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirmar Senha'}), 
        required=True,
        label='')

    def clean_username(self):
        return self.cleaned_data.get('username').strip().title()

    def clean(self):
        super(CadastrarForm, self).clean()
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if User.objects.filter(username=username).first():
            raise ValidationError('Usuário já existente')
        if password1 != password2:
            raise ValidationError('As senhas devem coincidir')
        

class Alterar_passwordForm(forms.Form):
    password_atual = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Senha atual'}), 
        required=True,
        label='')
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Nova senha'}), 
        required=True,
        label='')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirmar nova senha'}), 
        required=True,
        label='')
    
    def __init__(self, user: User, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        
    def clean(self) -> dict[str, Any]:
        super(Alterar_passwordForm, self).clean()

        password_atual = self.cleaned_data.get('password_atual')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not self.user.check_password(password_atual):
            raise ValidationError('Senha invalida')
        if password1 != password2:
            raise ValidationError('As senhas devem coincidir')
        if password1 == password_atual:
            raise ValidationError('Não é possível alterar para senha já existente')
        

class Alterar_usernameForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Novo nome'}), 
        required=True, 
        label='')
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirme sua senha'}), 
        required=True,
        label='')
    
    def __init__(self, user: User,*args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_username(self):
        return self.cleaned_data.get('username').strip().title()

    def clean(self):
        super(Alterar_usernameForm, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if not self.user.check_password(password):
            raise ('Senha inválida')
        if User.objects.filter(username=username):
            raise ValidationError('Nome já existente')

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Empresa',
                'class': 'titulo'
            })}
        labels = {
            'nome': ''
        }
    
    def clean_nome(self):
        return self.cleaned_data.get('nome').upper()

class ObrigacaoForm(forms.ModelForm):
    class Meta:
        model = Obrigacao
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Obrigação',
            })}
        labels = {
            'nome': ''
        }

    def clean_nome(self):
        return self.cleaned_data.get('nome').upper()

class CompetenciaForm(forms.ModelForm):
    tipo = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'competencia'}))
    class  Meta:
        model = Competencia
        fields = ['tipo', 'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro', 'obs']
        widgets = {field: forms.TextInput(attrs={'class': 'competencia', 'autocomplete':'off'}) for field in fields[:-1]}
        widgets.update({'obs': forms.Textarea(attrs={
            'class': 'competencia',
            'rows': 1})})
        labels = {field:'' for field in fields}
    
    def clean_tipo(self):
        return self.cleaned_data.get('tipo').upper()
        