from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')


def empresas(request, pagina=0):
    if pagina == 0:
        return redirect('empresas', 1)
    empresas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
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


def empresa(request, empresa):
    empresas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
    pagina = (empresas.index(empresa) // 12) + 1
    context = {
        'empresa': empresa,
        'pagina': pagina,
    }

    return render(request, 'empresa.html', context=context)


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


def obrigacao(request, obrigacao):
    return HttpResponse(f'olá {obrigacao}')


def competencias(request, pagina=0):
    if pagina == 0:
        return redirect('competencias', 1)
    competencias = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    competencias_selecionadas = competencias[pagina*12-12:pagina*12]
    anterior = pagina > 1
    sucesso = len(competencias) > pagina*12
    context = {
        'competencias': competencias_selecionadas,
        'anterior': anterior,
        'sucessor': sucesso,
        'pagina': pagina,
    }
    return render(request, 'competencias.html', context=context)

def competencia(request, competencia):
    return HttpResponse(f'olá {competencia}')