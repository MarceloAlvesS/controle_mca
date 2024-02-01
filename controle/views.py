from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Obrigacao, Empresa
import pandas as pd
from .utils import model_register


@login_required(login_url='/controle/login/')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='/controle/login/')
def empresas(request, pagina=0):
    if pagina == 0:
        return redirect('empresas', 1)
    empresas = Empresa.objects.filter(usuario=request.user)
    empresas_selecionadas = empresas[pagina*12-12:pagina*12]
    anterior = pagina > 1
    sucesso = len(empresas) > pagina*12
    context = {
        'empresas': empresas_selecionadas,
        'anterior': anterior,
        'sucessor': sucesso,
        'pagina': pagina,
    }

    return render(request, 'empresas.html', context=context)


@login_required(login_url='/controle/login/')
def empresa_view(request, empresa):
    context = {}
    empresa = Empresa.objects.filter(nome=empresa).first()
    if not empresa:
        return redirect('criar_empresa')
    competencias = empresa.competencias.all()
    

    if request.method == 'GET':
        empresaForm = EmpresaForm(instance=empresa)
        competenciaForm = CompetenciaForm()
        # competenciaForm_list = [CompetenciaForm(instance=competencia) for competencia in competencias]

    context['empresaForm'] = empresaForm
    # context['competenciaForm_list'] = competenciaForm_list
    context['competenciaForm'] = competenciaForm
    return render(request, 'empresa.html', context=context)


@login_required(login_url='/controle/login/')
def empresa_criar(request):
    context = {}
    if request.method == 'GET':
        empresaForm = EmpresaForm()
        competenciaForm = CompetenciaForm()
    elif request.method == 'POST':
        empresaForm = EmpresaForm(request.POST)
        if empresaForm.is_valid():
            nome = empresaForm.cleaned_data.get('nome')
            empresa = model_register(Empresa, usuario=request.user, nome=nome)
            post = dict(request.POST).copy()
            del post['nome']
            del post['csrfmiddlewaretoken']
            post = pd.DataFrame(post).to_dict(orient='records')
            for competencia in post:
                competenciaForm = CompetenciaForm(competencia)
                if competenciaForm.is_valid():
                    nome = competenciaForm.cleaned_data.get('tipo')
                    obrigacao = model_register(Obrigacao, nome=nome)
                    del competencia['tipo']
                    competencias = Competencia.objects.filter(empresa=empresa, obrigacao=obrigacao)
                    if competencias:
                        competencias.update(**competencia)
                    else:
                        empresa.obrigacoes.add(obrigacao, through_defaults=competencia) 
            return redirect('empresa', empresa)
                        


    context['empresaForm'] = EmpresaForm
    context['competenciaForm'] = CompetenciaForm
    return render(request, 'empresa.html', context=context)


@login_required(login_url='/controle/login/')
def obrigacoes(request, pagina=0):
    if pagina == 0:
        return redirect('obrigacoes', 1)
    obrigacoes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
    obrigacoes_selecionadas = obrigacoes[(pagina-1)*16:pagina*16]
    anterior = pagina > 1
    sucesso = len(obrigacoes) > pagina*16
    context = {
        'obrigacoes': obrigacoes_selecionadas,
        'anterior': anterior,
        'sucessor': sucesso,
        'pagina': pagina,
    }

    return render(request, 'obrigacoes.html', context=context)


@login_required(login_url='/controle/login/')
def obrigacao_view(request, obrigacao):
    return HttpResponse(f'olá {obrigacao}')


@login_required(login_url='/controle/login/')
def competencias(request):
    competencias = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    context = {
        'competencias': competencias,
    }
    return render(request, 'competencias.html', context=context)


@login_required(login_url='/controle/login/')
def competencia(request, competencia):
    return HttpResponse(f'olá {competencia}')


@login_required(login_url='/controle/login/')
def usuario(request):
    return render(request, 'user.html')


def login(request):
    context = {
        'tipo': 'login',
    }

    if request.method == 'GET':
        form = LoginForm()
        
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            login_django(request, authenticate(username=username, password=password))
            return redirect('home')
        
    context['form'] = form
    return render(request, 'login.html', context=context)
        

def cadastrar(request):
    context = {
        'tipo': 'cadastrar',
    }
    
    if request.method == 'GET':
        form = CadastrarForm()
    elif request.method == 'POST':
        form = CadastrarForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('login')
    context['form'] = form
    return render(request, 'login.html', context=context)
        

@login_required(login_url='/controle/login/')
def logout(request):
    logout_django(request)
    return redirect('login')


@login_required(login_url='/controle/login/')
def alterar_password(request):
    context = {
        'tipo': 'senha'
    }

    if request.method == 'GET':
        form = Alterar_passwordForm(request.user)
    elif request.method == 'POST':
        form = Alterar_passwordForm(request.user, request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            username = request.user.username
            user = request.user
            user.set_password(password1)
            user.save()
            login_django(request, authenticate(username=username, password=password1))
            return redirect('usuario')
    

    context['form'] = form
    return render(request, 'alterar_user.html', context=context)


@login_required(login_url='/controle/login/')
def alterar_username(request):
    context = {
        'tipo': 'username'
    }

    if request.method == 'GET':
        form = Alterar_usernameForm(request.user)
    
    elif request.method == 'POST':
        form = Alterar_usernameForm(request.user, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = request.user
            user.username =  username
            user.save()
            login_django(request, authenticate(username=username, password=password))
            return redirect('usuario')

    context['form'] = form
    return render(request, 'alterar_user.html', context=context)
    
