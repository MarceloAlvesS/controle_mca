from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def empresas(request):
    return render(request, 'home.html')

def obrigacoes(request):
    return render(request, 'home.html')

def competencias(request):
    return render(request, 'home.html')
