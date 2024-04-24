from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from controle.models import Empresa, Obrigacao, Competencia
from controle.forms import *
from controle.utils import *
from .utils import remove_object_model
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator, has_permission_decorator


@login_required(login_url=settings.LOGIN_URL)
@has_permission_decorator('ver_area_administrativa')
def home(request):
    context = {}

    return render(request, 'home_admin.html', context)


@has_role_decorator('administrador')
@login_required(login_url=settings.LOGIN_URL)
def clientes(request):
    match request.method:
        case 'POST':
            remove_object_model(Empresa, 'nome', request.POST.getlist('caixas_selecionadas'))

    context = {}
    context['tipo'] = {'plural':'clientes'}
    context['conteudos'] = Empresa.objects.all().order_by('nome')
    context['link'] = 'cliente_admin'
    return render(request, 'tipos_admin.html', context)


@has_role_decorator('administrador')
@login_required(login_url=settings.LOGIN_URL)
def cliente(request, cliente_nome):
    if not cliente_nome.isupper():
        return redirect('cliente_admin', cliente_nome.upper())
    
    context = {}
    
    try:
        empresa = Empresa.objects.get(nome=cliente_nome)
    except ObjectDoesNotExist:
        return redirect('clientes_admin')

    match request.method:
        case 'GET':
            tituloForm = create_dynamic_titulo_form('Empresa', ['nome', 'enquadramento'])(instance=empresa)
        case 'POST':
            tituloForm = create_dynamic_titulo_form('Empresa', ['nome', 'enquadramento'])(request.POST, instance=empresa)
            if tituloForm.is_valid():
                empresa.save()
                empresa = model_register(Empresa, **tituloForm.cleaned_data)

                competencias_anuais = get_competencias(POST=request.POST, names=['A-tipo', 'A-anual', 'A-obs'])
                competencias_mensais = get_competencias(POST=request.POST, names=['M-tipo', 'M-janeiro', 'M-fevereiro', 'M-marco', 'M-abril', 'M-maio', 'M-junho', 'M-julho', 'M-agosto', 'M-setembro', 'M-outubro', 'M-novembro', 'M-dezembro', 'M-obs'])
                deleted_competencias(empresa, competencias_anuais+competencias_mensais).delete()
                competenciasForm = get_forms_from_competencias(competencias_anuais=competencias_anuais, competencias_mensais=competencias_mensais)
                for form in competenciasForm:
                    competencia_register(formulario=form['competenciaForm'], model=Obrigacao, formato=form['formato'], empresa=empresa)
            else:
                print(tituloForm.errors)

    competencias_mensais = Competencia.objects.filter(empresa=empresa, obrigacao__formato='M').order_by('obrigacao__nome')
    competencias_anuais = Competencia.objects.filter(empresa=empresa, obrigacao__formato='A').order_by('obrigacao__nome')
    

    competenciasForm_list = [[CompetenciaMensalForm(tipo=competencia.obrigacao, instance=competencia) for competencia in competencias_mensais], [CompetenciaAnualForm(tipo=competencia.obrigacao, instance=competencia) for competencia in competencias_anuais]]
    formato_competenciasForm = [CompetenciaMensalForm, CompetenciaAnualForm] 
    for i, formato in enumerate(competenciasForm_list):
        if not formato:
            competenciasForm_list[i].append(formato_competenciasForm[i]())

    context['tipo'] = {'plural': 'clientes_admin', 'metodo':'editar'}
    context['tituloForm'] = tituloForm
    context['competenciaForm_list'] = competenciasForm_list
    if empresa.nome != cliente_nome:
        return redirect('cliente_admin', empresa.nome)
    return render(request, 'tipo_admin.html', context=context)


@has_role_decorator('administrador')
@login_required(login_url=settings.LOGIN_URL)
def competencias(request):
    context = {}
    context['tipo'] = {'plural':'competencias'}
    context['conteudos'] = Competencia.meses + ['anual']
    context['link'] = 'competencia_admin'
    return render(request, 'tipos_admin.html', context)


@has_role_decorator('administrador')
@login_required(login_url=settings.LOGIN_URL)
def competencia(request, mes):

    if not mes.islower():
        return redirect('competencia_admin', mes.lower())
    if not mes in Competencia.meses+['anual']:
        return redirect('competencias_admin')

    if mes == 'anual':
        formato = 'A'
    else:
        formato = 'M'

    context = {}

    empresas = Empresa.objects.all().distinct().order_by('enquadramento', 'nome')
    obrigacoes = Obrigacao.objects.filter(formato=formato).distinct().order_by('nome')
    
    tabela = {}
    for empresa in empresas:
        tabela[empresa] = []
        for obrigacao in obrigacoes:
            competencia = Competencia.objects.filter(empresa=empresa, obrigacao=obrigacao)
            valor_mes = competencia.values_list(mes).first()
            if valor_mes:
                if valor_mes[0]:
                    valor_mes = valor_mes[0]
                else:
                    valor_mes = ''
            else:
                valor_mes = '-'
            tabela[empresa].append(valor_mes)
    

    context['tipo'] = {'plural': 'competencias_admin'}
    context['mes'] = mes
    context['conteudo'] = {'tabela': tabela, 'obrigacoes': obrigacoes, 'empresas':empresas}
    return render(request, 'competencia_admin.html', context)


@login_required(login_url=settings.LOGIN_URL)
@has_role_decorator('administrador')
def obrigacoes(request):
    match request.method:
        case 'POST':
            remove_object_model(Obrigacao, 'nome', request.POST.getlist('caixas_selecionadas'))
    context = {}
    context['tipo'] = {'plural':'obrigações'}
    context['conteudos'] = Obrigacao.objects.all().order_by('nome')
    context['link'] = 'obrigacao_admin'
    return render(request, 'tipos_admin.html', context)


@has_role_decorator('administrador')
@login_required(login_url=settings.LOGIN_URL)
def obrigacao(request, obrigacao_nome):

    # Verificando se a obrigacao_name está na formatação correta
    if not obrigacao_nome.isupper():
        return redirect('obrigacao_admin', obrigacao_nome.upper())

    context = {}

    # verificando se a obrigação existe
    try:
        obrigacao = Obrigacao.objects.get(nome=obrigacao_nome)
    except ObjectDoesNotExist:
        return redirect('obrigacoes_admin', 1)


    # Casos para method GET e POST
    match request.method:
        case 'GET':
            # Atribuição dos form das obrigações
            tituloForm = create_dynamic_titulo_form('Obrigacao', ['nome', 'formato'])(instance=obrigacao)

        case 'POST':
            tituloForm = create_dynamic_titulo_form('Obrigacao', ['nome', 'formato'])(request.POST, instance=obrigacao)
            formato_antes = obrigacao.formato
            if tituloForm.is_valid():
                obrigacao.save()
                
                competencias = get_competencias(POST=request.POST, names=['M-tipo', 'M-janeiro', 'M-fevereiro', 'M-março', 'M-abril', 'M-maio', 'M-junho', 'M-julho', 'M-agosto', 'M-setembro', 'M-outubro', 'M-novembro', 'M-dezembro', 'M-obs'] if formato_antes == 'M' else ['A-tipo', 'A-anual', 'A-obs'])

                # Deletando competencias não encontradas no formulario
                deleted_competencias(obrigacao, competencias).delete()
                    
                competenciasForm = get_forms_from_competencias(competencias_anuais=competencias) if obrigacao.formato == 'A' else get_forms_from_competencias(competencias_mensais=competencias)
                for form in competenciasForm:
                    competencia_register(formulario=form['competenciaForm'], model=Empresa, obrigacao=obrigacao)

                return redirect('obrigacao_admin', obrigacao)
            else:
                print(tituloForm.errors)

    competencias = Competencia.objects.filter(obrigacao=obrigacao).order_by('empresa__nome')

    competenciasForm_list = [CompetenciaMensalForm(tipo=competencia.empresa, instance=competencia) if obrigacao.formato == 'M' else CompetenciaAnualForm(tipo=competencia.empresa, instance=competencia) for competencia in competencias]
    if not competenciasForm_list:
        competenciasForm_list = [CompetenciaMensalForm() if obrigacao.formato == 'M' else CompetenciaAnualForm()]


    context['tipo'] = {'plural': 'obrigacoes_admin', 'metodo':'editar', 'formato': obrigacao.formato}
    context['tituloForm'] = tituloForm

    context['competenciaForm_list'] = competenciasForm_list
    return render(request, 'tipo_admin.html', context=context)



@has_role_decorator('administrador')
@login_required(login_url=settings.LOGIN_URL)
def contabil(request):
    match request.method:
        case 'POST':
            remove_object_model(User, 'username', request.POST.getlist('caixas_selecionadas'))
    context = {}
    context['conteudos'] = User.objects.all().order_by('-groups', 'username').exclude(username='Admin')
    context['tipo'] = {'plural':'contabil'}
    context['link'] = 'home'
    return render(request, 'tipos_admin.html', context)
