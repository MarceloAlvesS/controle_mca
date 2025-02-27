from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from controle.forms import create_dynamic_titulo_form, CompetenciaAnualForm
from controle.forms import CompetenciaMensalForm, DuplicarDadosForm
from controle.models import Obrigacao, Empresa, Competencia
from django.contrib.auth.models import User
from controle import utils
from django.conf import settings


@login_required(login_url=settings.LOGIN_URL)
@utils.check_permission(permission='ver_funcionarios')
def home(request, client):
    context = {'client': client}
    return render(request, 'home.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@utils.check_permission(permission='ver_funcionarios')
def clientes(request, client, pagina=0):
    context = {'client': client}

    if pagina == 0:
        return redirect('clientes', client, 1)

    usuario = utils.get_user_from(client)
    empresas = usuario.empresas.distinct().order_by('nome')
    selecionados = utils.get_tipos(empresas, pagina, 12)

    context.update({
        'conteudos': selecionados['empresas_selecionadas'],
        'anterior': selecionados['anterior'],
        'sucessor': selecionados['sucesso'],
        'pagina': pagina,
        'ano': settings.ANO_ATUAL,
        'tipo': {'singular': 'cliente',
                 'plural': 'clientes',
                 'correcao': 'clientes'}
    })

    return render(request, 'tipos.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@utils.check_permission(permission='ver_funcionarios')
def criar_cliente(request, client):
    context = {'client': client}
    usuario = utils.get_user_from(client)

    formularios = {
        'titulo': create_dynamic_titulo_form(model_name='Empresa',
                                             fields=['nome', 'enquadramento']),
        'competencia_mensal': CompetenciaMensalForm,
        'competencia_anual': CompetenciaAnualForm,
    }

    match request.method:
        case 'GET':
            tituloForm = formularios['titulo'](auto_id='id_%s_editavel')

        case 'POST':
            tituloForm = formularios['titulo'](request.POST,
                                               auto_id='id_%s_editavel')
            if tituloForm.is_valid():
                empresa = utils.model_register(
                    Empresa,
                    **tituloForm.cleaned_data,
                    ano_inscricao = settings.ANO_ATUAL)

                competencias_anuais = utils.get_competencias(
                    POST=request.POST,
                    names=['A-tipo', 'A-anual', 'A-obs'])
                competencias_mensais = utils.get_competencias(
                    POST=request.POST,
                    names=['M-tipo',
                           'M-janeiro',
                           'M-fevereiro',
                           'M-marco',
                           'M-abril',
                           'M-maio',
                           'M-junho',
                           'M-julho',
                           'M-agosto',
                           'M-setembro',
                           'M-outubro',
                           'M-novembro',
                           'M-dezembro',
                           'M-obs'])

                competenciasForm = utils.get_forms_from_competencias(
                    competencias_anuais=competencias_anuais,
                    competencias_mensais=competencias_mensais)
                for form in competenciasForm:
                    utils.competencia_register(
                        formulario = form['competenciaForm'],
                        model = Obrigacao,
                        formato = form['formato'],
                        empresa = empresa,
                        usuario = usuario,
                        ano = settings.ANO_ATUAL)

                return redirect('editar_cliente', client, settings.ANO_ATUAL, empresa)
            else:
                print(tituloForm.errors)
    competenciaForm_list = [[formularios['competencia_mensal']()],
                            [formularios['competencia_anual']()]]
    context['tipo'] = {'plural': 'clientes', 'metodo': 'criar'}
    context['tituloForm'] = tituloForm
    context['competenciaForm_list'] = competenciaForm_list
    context['pagina'] = 1
    return render(request, 'tipo.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@utils.check_permission(permission='ver_funcionarios')
def editar_cliente(request, ano, client, cliente_nome):
    if not cliente_nome.isupper():
        return redirect('editar_cliente', client, ano, cliente_nome.upper())
    context = {'client': client,
               'ano': ano}
    usuario = utils.get_user_from(client)
    try:
        empresa = usuario.empresas.distinct().get(nome=cliente_nome)
    except ObjectDoesNotExist:
        return redirect('clientes', client, 1)
    empresas = usuario.empresas.distinct().order_by('nome')
    pagina = int(list(empresas).index(empresa)/12)+1
    match request.method:
        case 'GET':
            tituloForm = create_dynamic_titulo_form(
                'Empresa',
                ['nome', 'enquadramento']
                )(instance=empresa)
        case 'POST':
            tituloForm = create_dynamic_titulo_form(
                'Empresa',
                ['nome', 'enquadramento']
                )(request.POST, instance=empresa)
            if tituloForm.is_valid():
                empresa.save()
                empresa = utils.model_register(
                    Empresa,
                    **tituloForm.cleaned_data)

                competencias_anuais = utils.get_competencias(POST=request.POST,
                                                             names=['A-tipo',
                                                                    'A-anual',
                                                                    'A-obs'])
                competencias_mensais = utils.get_competencias(
                    POST=request.POST,
                    names=['M-tipo',
                           'M-janeiro',
                           'M-fevereiro',
                           'M-marco',
                           'M-abril',
                           'M-maio',
                           'M-junho',
                           'M-julho',
                           'M-agosto',
                           'M-setembro',
                           'M-outubro',
                           'M-novembro',
                           'M-dezembro',
                           'M-obs'])
                utils.deleted_competencias(
                    model = empresa,
                    ano = ano,
                    competencias_post = competencias_anuais+competencias_mensais,
                    usuario = usuario).delete()
                competenciasForm = utils.get_forms_from_competencias(
                    competencias_anuais=competencias_anuais,
                    competencias_mensais=competencias_mensais)
                for form in competenciasForm:
                    utils.competencia_register(
                        formulario = form['competenciaForm'],
                        model = Obrigacao,
                        formato = form['formato'],
                        empresa = empresa,
                        usuario = usuario,
                        ano = ano)
            else:
                print(tituloForm.errors)

    competencias_mensais = Competencia.objects.filter(
        empresa=empresa,
        usuario=usuario,
        obrigacao__formato='M',
        ano=ano).order_by('obrigacao__nome')
    competencias_anuais = Competencia.objects.filter(
        empresa=empresa,
        usuario=usuario,
        obrigacao__formato='A',
        ano=ano).order_by('obrigacao__nome')

    competenciasForm_list = [
        [CompetenciaMensalForm(
            tipo=competencia.obrigacao,
            instance=competencia) for competencia in competencias_mensais],
        [CompetenciaAnualForm(
            tipo=competencia.obrigacao,
            instance=competencia) for competencia in competencias_anuais]]
    formato_competenciasForm = [CompetenciaMensalForm, CompetenciaAnualForm]
    for i, formato in enumerate(competenciasForm_list):
        if not formato:
            competenciasForm_list[i].append(formato_competenciasForm[i]())

    context['tipo'] = {
        'singular': 'cliente',
        'plural': 'clientes',
        'metodo': 'editar'}
    context['tituloForm'] = tituloForm
    context['competenciaForm_list'] = competenciasForm_list
    context['pagina'] = pagina
    context['datas'] = range(int(empresa.ano_inscricao), settings.ANO_ATUAL+1)

    if empresa.nome != cliente_nome:
        return redirect('editar_cliente', client, ano, empresa.nome)
    return render(request, 'tipo.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@utils.check_permission(permission='ver_funcionarios')
def obrigacoes(request, client, pagina=0):
    context = {'client': client}
    if pagina == 0:
        return redirect('obrigacoes', client, 1)
    usuario = utils.get_user_from(client)
    obrigacoes = usuario.obrigacoes.distinct().order_by('nome')
    obrigacoes_selecionadas = obrigacoes[(pagina-1)*16:pagina*16]
    context.update({
        'conteudos': obrigacoes_selecionadas,
        'anterior': pagina > 1,
        'sucessor': len(obrigacoes) > pagina*16,
        'pagina': pagina,
        'ano': settings.ANO_ATUAL,
        'tipo': {'plural': 'obrigacoes',
                 'singular': 'obrigacao',
                 'correcao': 'obrigações'}
    })

    return render(request, 'tipos.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@utils.check_permission(permission='ver_funcionarios')
def criar_obrigacao(request, client):
    context = {'client': client}
    usuario = utils.get_user_from(client)
    formularios = {
        'titulo': create_dynamic_titulo_form(
            model_name='Obrigacao',
            fields=['nome', 'formato']),
        'competencia_mensal': CompetenciaMensalForm,
        'competencia_anual': CompetenciaAnualForm,
    }
    match request.method:
        case 'GET':
            tituloForm = formularios['titulo']()

        case 'POST':
            tituloForm = formularios['titulo'](request.POST)
            if tituloForm.is_valid():
                obrigacao = utils.model_register(
                    Obrigacao,
                    **tituloForm.cleaned_data,
                    ano_inscricao = settings.ANO_ATUAL)
                competencias = utils.get_competencias(
                    POST=request.POST,
                    names=['M-tipo',
                           'M-janeiro',
                           'M-fevereiro',
                           'M-marco',
                           'M-abril',
                           'M-maio',
                           'M-junho',
                           'M-julho',
                           'M-agosto',
                           'M-setembro',
                           'M-outubro',
                           'M-novembro',
                           'M-dezembro',
                           'M-obs'] if obrigacao.formato == 'M' else [
                                                                     'A-tipo',
                                                                     'A-anual',
                                                                     'A-obs'])
                match obrigacao.formato:
                    case 'A':
                        competenciasForm = utils.get_forms_from_competencias(
                            competencias_anuais=competencias)
                    case 'M':
                        competenciasForm = utils.get_forms_from_competencias(
                            competencias_mensais=competencias)
                for form in competenciasForm:
                    utils.competencia_register(
                        formulario=form['competenciaForm'],
                        model=Empresa, obrigacao=obrigacao,
                        usuario=usuario,
                        ano = settings.ANO_ATUAL)

                return redirect('editar_obrigacao', client, settings.ANO_ATUAL, obrigacao)
            else:
                print(tituloForm.errors)

    competenciaForm_list = [
        [formularios['competencia_mensal']()],
        [formularios['competencia_anual']()]]
    context['tipo'] = {
        'plural': 'obrigacoes',
        'metodo': 'criar'}
    context['tituloForm'] = tituloForm
    context['competenciaForm_list'] = competenciaForm_list
    context['pagina'] = 1
    return render(request, 'tipo.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@utils.check_permission(permission='ver_funcionarios')
def editar_obrigacao(request, ano, client, obrigacao_nome):

    # Verificando se a obrigacao_name está na formatação correta
    if not obrigacao_nome.isupper():
        return redirect('editar_obrigacao', client, ano, obrigacao_nome.upper())
    # variaveis padrões
    context = {'client': client,
               'ano': ano}
    usuario = utils.get_user_from(client)

    # verificando se a obrigação existe
    try:
        obrigacao = usuario.obrigacoes.distinct().get(nome=obrigacao_nome)
    except ObjectDoesNotExist:
        return redirect('obrigacoes', client, 1)

    obrigacoes_objects = usuario.obrigacoes.distinct().order_by('nome')
    pagina = int(list(obrigacoes_objects).index(obrigacao)/16) + 1

    # Casos para method GET e POST
    match request.method:
        case 'GET':
            # Atribuição dos form das obrigações
            tituloForm = create_dynamic_titulo_form(
                'Obrigacao',
                ['nome', 'formato'])(instance=obrigacao)

        case 'POST':
            tituloForm = create_dynamic_titulo_form(
                'Obrigacao',
                ['nome', 'formato'])(request.POST, instance=obrigacao)
            formato_antes = obrigacao.formato
            if tituloForm.is_valid():
                obrigacao.save()
                competencias = utils.get_competencias(
                    POST=request.POST,
                    names=['M-tipo',
                           'M-janeiro',
                           'M-fevereiro',
                           'M-fevereiro',
                           'M-marco',
                           'M-abril',
                           'M-maio',
                           'M-junho',
                           'M-julho',
                           'M-agosto',
                           'M-setembro',
                           'M-outubro',
                           'M-novembro',
                           'M-dezembro',
                           'M-obs'] if formato_antes == 'M' else ['A-tipo',
                                                                  'A-anual',
                                                                  'A-obs'])

                # Deletando competencias não encontradas no formulario
                utils.deleted_competencias(
                    model = obrigacao,
                    ano = ano,
                    competencias_post = competencias,
                    usuario = usuario).delete()
                match obrigacao.formato:
                    case 'A':
                        competenciasForm = utils.get_forms_from_competencias(
                            competencias_anuais=competencias)
                    case 'M':
                        competenciasForm = utils.get_forms_from_competencias(
                            competencias_mensais=competencias)
                for form in competenciasForm:
                    utils.competencia_register(
                        formulario = form['competenciaForm'],
                        model = Empresa,
                        obrigacao = obrigacao,
                        usuario = usuario,
                        ano = ano)

                return redirect('editar_obrigacao', client, ano, obrigacao)
            else:
                print(tituloForm.errors)

    competencias = Competencia.objects.filter(
        obrigacao=obrigacao,
        usuario=usuario,
        ano=ano).order_by('empresa__nome')
    match obrigacao.formato:
        case 'A':
            competenciasForm_list = [CompetenciaAnualForm(
                tipo=competencia.empresa,
                instance=competencia) for competencia in competencias]
        case 'M':
            competenciasForm_list = [CompetenciaMensalForm(
                tipo=competencia.empresa,
                instance=competencia) for competencia in competencias]
    if not competenciasForm_list:
        match obrigacao.formato:
            case 'A':
                CompetenciaAnualForm()
            case 'M':
                CompetenciaMensalForm()

    context['tipo'] = {'singular': 'obrigacao',
                       'plural': 'obrigacoes',
                       'metodo': 'editar',
                       'formato': obrigacao.formato}
    context['tituloForm'] = tituloForm
    context['pagina'] = pagina
    context['competenciaForm_list'] = competenciasForm_list
    context['datas'] = range(
        int(obrigacao.ano_inscricao),
        settings.ANO_ATUAL+1)
    return render(request, 'tipo.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@utils.check_permission(permission='ver_funcionarios')
def competencias(request, client):
    context = {'client': client}
    competencias = Competencia.meses + ['anual']
    context.update({
        'tipo': {'plural': 'competencias',
                 'singular': 'competencia',
                 'correcao': 'competencias'},
        'ano': settings.ANO_ATUAL,
        'conteudos': competencias
    })
    return render(request, 'tipos.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
@utils.check_permission(permission='ver_funcionarios')
def visualizar_competencia(request,
                           ano: int,
                           client: str,
                           mes: str) -> HttpResponse:
    if not mes.islower():
        return redirect('editar_competencia', client, ano, mes.lower())
    if mes not in Competencia.meses + ['anual']:
        return redirect('competencias', client)

    if mes == 'anual':
        formato = 'A'
    else:
        formato = 'M'

    context = {'client': client,
               'ano': ano}

    usuario = utils.get_user_from(client)
    empresas = usuario.empresas.all().distinct().order_by('nome')
    obrigacoes = usuario.obrigacoes.filter(
        formato=formato).distinct().order_by('nome')
    tabela = {}
    for empresa in empresas:
        tabela[empresa] = []
        for obrigacao in obrigacoes:
            competencia = Competencia.objects.filter(
                empresa=empresa,
                obrigacao=obrigacao,
                usuario=usuario,
                ano=ano)
            valor_mes = competencia.values_list(mes).first()
            if valor_mes:
                if valor_mes[0]:
                    valor_mes = valor_mes[0]
                else:
                    valor_mes = ''
            else:
                valor_mes = '-'
            tabela[empresa].append(valor_mes)

    context['tipo'] = {'plural': 'competencias', 'singular': 'competencia'}
    context['mes'] = mes
    context['conteudo'] = {
        'tabela': tabela,
        'obrigacoes': obrigacoes,
        'empresas': empresas}
    context['datas'] = range(settings.ANO_INICIAL, settings.ANO_ATUAL+1)
    return render(request, 'competencia.html', context)


@login_required(login_url=settings.LOGIN_URL)
def duplicar_dados(request, client: str) -> HttpResponse:
    usuario = utils.get_user_from(client)
    context: dict[str: any] = {
        'client': client,
        'sucess_list': [],
        'usuario': usuario}

    match request.method:
        case 'GET':
            form = DuplicarDadosForm()
        case 'POST':
            form = DuplicarDadosForm(request.POST)
            if form.is_valid():
                def duplicate_competencia(
                        competencia: Competencia) -> Competencia:
                    retuned = Competencia.objects.get_or_create(
                        ano=para_ano,
                        empresa=competencia.empresa,
                        obrigacao=competencia.obrigacao,
                        usuario=competencia.usuario,
                        defaults=meses)
                    print(f'{retuned} processado!!')
                    return retuned
                meses = {mes: '' for mes in Competencia.meses+['anual']}
                de_ano = form.cleaned_data['de_ano']
                para_ano = form.cleaned_data['para_ano']
                if usuario.has_perm('ver_area_administrativa'):
                    competencias = Competencia.objects.filter(ano = de_ano)
                else:
                    competencias = Competencia.objects.filter(ano = de_ano, usuario = usuario)
                _ = list(map(duplicate_competencia, competencias))
                context['sucess_list'].append('Datos transferidos do ano ' +
                                              f'{de_ano} para ano {para_ano}' +
                                              'com sucesso')

    context['form'] = form
    return render(request, 'duplicar.html', context=context)
