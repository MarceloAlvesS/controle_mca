from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_permission
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone

@login_required(login_url=settings.LOGIN_URL)
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
            user = authenticate(username=username, password=password)
            login_django(request, user)

            if user:
                sessions = Session.objects.filter(expire_date__gt=timezone.now())
                sessions.exclude(session_key=request.session.session_key).delete()

            if has_permission(request.user, 'ver_area_administrativa'):
                return redirect('home_admin')
            return redirect('home', request.user)
        
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
            assign_role(user, 'contabil')

            return redirect('login')
    context['form'] = form
    return render(request, 'login.html', context=context)
        

@login_required(login_url=settings.LOGIN_URL)
def logout(request):
    logout_django(request)
    return redirect('login')


@login_required(login_url=settings.LOGIN_URL)
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


@login_required(login_url=settings.LOGIN_URL)
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
