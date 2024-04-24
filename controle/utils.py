from django.db.models import Model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rolepermissions.checkers import has_permission
from django.shortcuts import redirect
from controle.models import *
from controle.forms import *


def model_register(model: Model, **kwargs):
    nome = kwargs.pop('nome')
    tipo = model.objects.update_or_create(nome=nome, defaults=kwargs)
    return tipo[0]
    

def difference_from(dictionary, differences:list):
    dictionary = dictionary.copy()
    for difference in differences:
        dictionary.pop(difference, '')
    return dictionary

def get_user_from(client):
    return User.objects.filter(username=client).first()

def user_verificatin(client, user):
    return client == user


def check_permission(permission):
    def decorator(func):
        def validacao(request, *args, **kwargs):
            if not User.objects.filter(username=kwargs.get('client')).first() or (not(has_permission(request.user, permission)) and request.user.username != kwargs.get('client')):
                kwargs['client'] = request.user
                return redirect(request.resolver_match.url_name, **kwargs)
            return func(request, *args, **kwargs)
        return validacao
    return decorator


def get_tipos(empresas, page, quant):
    returned = {}
    returned['empresas_selecionadas'] = empresas[(page-1)*quant:page*quant]
    returned['anterior'] = page > 1
    returned['sucesso'] = len(empresas) > page*quant
    return returned


def get_values_from_keys(dicionario, *keys):
    returned = {key: dicionario.get(key) for key in keys}
    return returned

def get_competencias(POST, names:list):
    returned = []
    post = {name:POST.getlist(name) for name in names}
    for index, _ in enumerate(post[names[0]]):
        competencia = {}
        for name in names:
            competencia[name] = post[name][index]
        returned.append(competencia)
    return returned


def competencia_register(formulario, model, formato='M', **dependencias):
    if formulario.is_valid():
        nome = formulario.cleaned_data.pop('tipo')
        registrador = {
            Obrigacao: lambda: model_register(Obrigacao, nome=nome, formato=formato),
            Empresa: lambda: model_register(Empresa, nome=nome)
        }
        dependencias[model.__name__.lower()] = registrador[model]()
        Competencia.objects.update_or_create(**dependencias, defaults=formulario.cleaned_data)


def get_forms_from_competencias(competencias_anuais=[], competencias_mensais=[]):
    returned = []
    competencias = competencias_anuais + competencias_mensais
    for index, competencia in enumerate(competencias, start=1):
        formato = 'A' if index <= len(competencias_anuais) else 'M'
        competenciaForm = CompetenciaAnualForm(competencia) if formato == 'A' else CompetenciaMensalForm(competencia)
        returned.append({'competenciaForm': competenciaForm, 'formato':formato})
    return returned


def deleted_competencias(model, competencias_post, usuario=None):
    selecionador = {
        Empresa: 'obrigacao__nome',
        Obrigacao: 'empresa__nome'
    }
    competencias_post_nomes = set((post[list(post.keys())[0]] for post in competencias_post))
    returned = model.competencias.exclude(**{selecionador[type(model)]+'__in':competencias_post_nomes})

    # Caso seja dado como parâmetro o usuario será filtrado das competencias faltantes apenas aquelas que há o usuario dado
    if usuario:
        returned = returned.filter(usuario=usuario)

    return returned


