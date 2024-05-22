from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from controle.forms import *
from controle.models import Obrigacao, Empresa, Competencia
from controle.utils import *
from django.conf import settings

@login_required(login_url=settings.LOGIN_URL)
@check_permission(permission='ver_funcionarios')
def home(request, client):
    context = {'client': client}
    return render(request, 'home.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@check_permission(permission='ver_funcionarios')
def clientes(request, client, pagina=0):
    context = {'client': client}

    if pagina == 0:
        return redirect('clientes', client, 1)

    usuario = get_user_from(client)
    empresas = usuario.empresas.distinct().order_by('nome')
    selecionados = get_tipos(empresas, pagina, 12)

    context.update({
        'conteudos': selecionados['empresas_selecionadas'],
        'anterior': selecionados['anterior'],
        'sucessor': selecionados['sucesso'],
        'pagina': pagina,
        'tipo': {'singular': 'cliente',
                 'plural': 'clientes',
                 'correcao': 'clientes'}
    })

    return render(request, 'tipos.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@check_permission(permission='ver_funcionarios')
def criar_cliente(request, client):
    context = {'client': client}
    usuario = get_user_from(client)

    formularios = {
        'titulo':create_dynamic_titulo_form(model_name='Empresa', fields=['nome', 'enquadramento']),
        'competencia_mensal': CompetenciaMensalForm,
        'competencia_anual': CompetenciaAnualForm,
    }

    match request.method:
        case 'GET':
            tituloForm = formularios['titulo'](auto_id='id_%s_editavel')

        case 'POST':
            tituloForm = formularios['titulo'](request.POST, auto_id='id_%s_editavel')
            if tituloForm.is_valid():
                empresa = model_register(Empresa, **tituloForm.cleaned_data)

                competencias_anuais = get_competencias(POST=request.POST, names=['A-tipo', 'A-anual', 'A-obs'])
                competencias_mensais = get_competencias(POST=request.POST, names=['M-tipo', 'M-janeiro', 'M-fevereiro', 'M-marco', 'M-abril', 'M-maio', 'M-junho', 'M-julho', 'M-agosto', 'M-setembro', 'M-outubro', 'M-novembro', 'M-dezembro', 'M-obs'])

                competenciasForm = get_forms_from_competencias(competencias_anuais=competencias_anuais, competencias_mensais=competencias_mensais)
                for form in competenciasForm:
                    competencia_register(formulario=form['competenciaForm'], model=Obrigacao, formato=form['formato'], empresa=empresa, usuario=usuario)

                return redirect('editar_cliente', client, empresa)
            else:
                print(tituloForm.errors)
            
    competenciaForm_list = [[formularios['competencia_mensal']()],[formularios['competencia_anual']()]]
    context['tipo'] = {'plural':'clientes', 'metodo': 'criar'}
    context['tituloForm'] = tituloForm
    context['competenciaForm_list'] = competenciaForm_list
    context['pagina'] = 1
    return render(request, 'tipo.html', context=context)
            

@login_required(login_url=settings.LOGIN_URL)
@check_permission(permission='ver_funcionarios')
def editar_cliente(request, client, cliente_nome):
    if not cliente_nome.isupper():
        return redirect('editar_cliente', client, cliente_nome.upper())
    
    context = {'client': client}
    usuario = get_user_from(client)
    
    try:
        empresa = usuario.empresas.distinct().get(nome=cliente_nome)
    except ObjectDoesNotExist:
        return redirect('clientes', client, 1)
    
    pagina = int(list(usuario.empresas.distinct().order_by('nome')).index(empresa)/12)+1
    print(list(usuario.empresas.distinct().order_by('nome')).index(empresa))
    
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
                deleted_competencias(empresa, competencias_anuais+competencias_mensais, usuario).delete()
                competenciasForm = get_forms_from_competencias(competencias_anuais=competencias_anuais, competencias_mensais=competencias_mensais)
                for form in competenciasForm:
                    competencia_register(formulario=form['competenciaForm'], model=Obrigacao, formato=form['formato'], empresa=empresa, usuario=usuario)
            else:
                print(tituloForm.errors)

    competencias_mensais = Competencia.objects.filter(empresa=empresa, usuario=usuario, obrigacao__formato='M').order_by('obrigacao__nome')
    competencias_anuais = Competencia.objects.filter(empresa=empresa, usuario=usuario, obrigacao__formato='A').order_by('obrigacao__nome')
    

    competenciasForm_list = [[CompetenciaMensalForm(tipo=competencia.obrigacao, instance=competencia) for competencia in competencias_mensais], [CompetenciaAnualForm(tipo=competencia.obrigacao, instance=competencia) for competencia in competencias_anuais]]
    formato_competenciasForm = [CompetenciaMensalForm, CompetenciaAnualForm] 
    for i, formato in enumerate(competenciasForm_list):
        if not formato:
            competenciasForm_list[i].append(formato_competenciasForm[i]())

    context['tipo'] = {'plural': 'clientes', 'metodo':'editar'}
    context['tituloForm'] = tituloForm
    context['competenciaForm_list'] = competenciasForm_list
    context['pagina'] = pagina
    if empresa.nome != cliente_nome:
        return redirect('editar_cliente', client, empresa.nome)
    return render(request, 'tipo.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@check_permission(permission='ver_funcionarios')
def obrigacoes(request, client, pagina=0):
    context = {'client': client}
    if pagina == 0:
        return redirect('obrigacoes', client, 1)
    
    usuario = get_user_from(client)
    obrigacoes = usuario.obrigacoes.distinct().order_by('nome')
    obrigacoes_selecionadas = obrigacoes[(pagina-1)*16:pagina*16]
    context.update({
        'conteudos': obrigacoes_selecionadas,
        'anterior': pagina > 1,
        'sucessor': len(obrigacoes) > pagina*16,
        'pagina': pagina,
        'tipo': {'plural':'obrigacoes', 
                 'singular':'obrigacao', 
                 'correcao':'obrigações'}
    })

    return render(request, 'tipos.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@check_permission(permission='ver_funcionarios')
def criar_obrigacao(request, client):
    context = {'client': client}
    usuario = get_user_from(client)
    
    formularios = {
        'titulo': create_dynamic_titulo_form(model_name='Obrigacao', fields=['nome', 'formato']),
        'competencia_mensal': CompetenciaMensalForm,
        'competencia_anual': CompetenciaAnualForm,
    } 
    match request.method:
        case 'GET':
            tituloForm = formularios['titulo']()

        case 'POST':
            tituloForm = formularios['titulo'](request.POST)
            if tituloForm.is_valid():
                obrigacao = model_register(Obrigacao, **tituloForm.cleaned_data)
                
                competencias = get_competencias(POST=request.POST, names=['M-tipo', 'M-janeiro', 'M-fevereiro', 'M-marco', 'M-abril', 'M-maio', 'M-junho', 'M-julho', 'M-agosto', 'M-setembro', 'M-outubro', 'M-novembro', 'M-dezembro', 'M-obs'] if obrigacao.formato == 'M' else ['A-tipo', 'A-anual', 'A-obs'])

                competenciasForm = get_forms_from_competencias(competencias_anuais=competencias) if obrigacao.formato == 'A' else get_forms_from_competencias(competencias_mensais=competencias)
                for form in competenciasForm:
                    competencia_register(formulario=form['competenciaForm'], model=Empresa, obrigacao=obrigacao, usuario=usuario)

                return redirect('editar_obrigacao', client, obrigacao)
            else:
                print(tituloForm.errors)

    competenciaForm_list =  [[formularios['competencia_mensal']()], [formularios['competencia_anual']()]]
    context['tipo'] = {'plural': 'obrigacoes', 'metodo':'criar'}
    context['tituloForm'] = tituloForm
    context['competenciaForm_list'] = competenciaForm_list
    context['pagina'] = 1
    return render(request, 'tipo.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@check_permission(permission='ver_funcionarios')
def editar_obrigacao(request, client, obrigacao_nome):

    # Verificando se a obrigacao_name está na formatação correta
    if not obrigacao_nome.isupper():
        return redirect('editar_obrigacao', client, obrigacao_nome.upper())
    
    # variaveis padrões
    context = {'client': client}
    usuario = get_user_from(client)

    # verificando se a obrigação existe
    try:
        obrigacao = usuario.obrigacoes.distinct().get(nome=obrigacao_nome)
    except ObjectDoesNotExist:
        return redirect('obrigacoes', client, 1)

    pagina = int(list(usuario.obrigacoes.distinct().order_by('nome')).index(obrigacao)/16) + 1

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
                
                competencias = get_competencias(POST=request.POST, names=['M-tipo', 'M-janeiro', 'M-fevereiro', 'M-marco', 'M-abril', 'M-maio', 'M-junho', 'M-julho', 'M-agosto', 'M-setembro', 'M-outubro', 'M-novembro', 'M-dezembro', 'M-obs'] if formato_antes == 'M' else ['A-tipo', 'A-anual', 'A-obs'])

                # Deletando competencias não encontradas no formulario
                deleted_competencias(obrigacao, competencias, usuario).delete()
                    
                competenciasForm = get_forms_from_competencias(competencias_anuais=competencias) if obrigacao.formato == 'A' else get_forms_from_competencias(competencias_mensais=competencias)
                for form in competenciasForm:
                    competencia_register(formulario=form['competenciaForm'], model=Empresa, obrigacao=obrigacao, usuario=usuario)

                return redirect('editar_obrigacao', client, obrigacao)
            else:
                print(tituloForm.errors)

    competencias = Competencia.objects.filter(obrigacao=obrigacao, usuario=usuario).order_by('empresa__nome')

    competenciasForm_list = [CompetenciaMensalForm(tipo=competencia.empresa, instance=competencia) if obrigacao.formato == 'M' else CompetenciaAnualForm(tipo=competencia.empresa, instance=competencia) for competencia in competencias]
    if not competenciasForm_list:
        competenciasForm_list = [CompetenciaMensalForm() if obrigacao.formato == 'M' else CompetenciaAnualForm()]


    context['tipo'] = {'plural': 'obrigacoes', 'metodo':'editar', 'formato': obrigacao.formato}
    context['tituloForm'] = tituloForm
    context['pagina'] = pagina
    context['competenciaForm_list'] = competenciasForm_list
    return render(request, 'tipo.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@check_permission(permission='ver_funcionarios')
def competencias(request, client):
    context = {'client': client}
    competencias = Competencia.meses + ['anual']
    context.update({
        'tipo': {'plural':'competencias', 
                 'singular':'competencia', 
                 'correcao':'competencias'},
        'conteudos': competencias
    })
    return render(request, 'tipos.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@check_permission(permission='ver_funcionarios')
def visualizar_competencia(request, client, mes:str):
    if not mes.islower():
        return redirect('editar_competencia', client, mes.lower())
    if not mes in Competencia.meses + ['anual']:
        return redirect('competencias', client)

    if mes == 'anual':
        formato = 'A'
    else:
        formato = 'M'

    context = {'client': client}

    usuario = get_user_from(client)

    empresas = usuario.empresas.all().distinct().order_by('enquadramento', 'nome')
    obrigacoes = usuario.obrigacoes.filter(formato=formato).distinct().order_by('nome')
    
    tabela = {}
    for empresa in empresas:
        tabela[empresa] = []
        for obrigacao in obrigacoes:
            competencia = Competencia.objects.filter(empresa=empresa, obrigacao=obrigacao, usuario=usuario)
            valor_mes = competencia.values_list(mes).first()
            if valor_mes:
                if valor_mes[0]:
                    valor_mes = valor_mes[0]
                else:
                    valor_mes = ''
            else:
                valor_mes = '-'
            tabela[empresa].append(valor_mes)
    

    context['tipo'] = ['competencias']
    context['mes'] = mes
    context['conteudo'] = {'tabela': tabela, 'obrigacoes': obrigacoes, 'empresas':empresas}
    return render(request, 'competencia.html', context)
