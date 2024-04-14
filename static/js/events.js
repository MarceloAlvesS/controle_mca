function limpar_linha(linha) {
  for (let i=0; i < linha.children.length; i++){
    if (linha.children[i].children[0]) {
      linha.children[i].children[0].value = ''
    }
  }
  return linha
}

function adicionar_linha(event, linha) {
  if (event) {
    event.preventDefault()
  }
  let linha_clonada = linha.cloneNode(true)
  linha_clonada.children[0].children[1].addEventListener('click', deletar) 
  
  event.target.parentElement.parentElement.append(linha_clonada)
}

function adicionar_evento(elementos, evento, funcao) {
  for (let index = 0; index < elementos.length; index++) {
    elementos[index].addEventListener(evento, funcao)
  }
}

function deletar(event) {
  if(event) {
    event.preventDefault()
  }
  let tabela = event.target.parentElement.parentElement.parentElement
  let linha = event.target.parentElement.parentElement
  tabela.removeChild(linha)
}

function deletar_linhas(event) {
  if (event) {
    event.preventDefault()
  }
  let tabela = event.target.parentElement.parentElement
  while (tabela.children[2]) {
    tabela.removeChild(tabela.children[2])
  }
}

function enquadrar(event) {
  if (event) {
    event.preventDefault()
  }
  document.querySelectorAll('.excluir').forEach(element => {
      element.click()
  });
  let valor = event.target.value
  let enquadramento = enquadramentos[valor]
  for (let obrigacao in enquadramento[0]) {
    let linha = linha_mensal.cloneNode(true)
    linha.children[0].children[0].value = enquadramento[0].sort()[obrigacao].toUpperCase()
    linha.children[0].children[1].addEventListener('click', deletar) 
    document.getElementById('mensal').appendChild(linha)
  }
  for (let obrigacao in enquadramento[1]) {
    let linha = linha_anual.cloneNode(true)
    linha.children[0].children[0].value = enquadramento[1].sort()[obrigacao].toUpperCase()
    linha.children[0].children[1].addEventListener('click', deletar) 

    document.getElementById('anual').appendChild(linha)
  }
}

document.querySelectorAll('.excluir').forEach(element => {
  element.addEventListener('click', function(event) {
    deletar_linhas(event)})
})

let linha_mensal = '';
let linha_anual = '';

if (document.getElementById('mensal')){
  linha_mensal = limpar_linha(document.getElementById('mensal').children[2].cloneNode(true));
}
if (document.getElementById('anual')){
  linha_anual = limpar_linha(document.getElementById('anual').children[2].cloneNode(true));
}

const escolha = {'mensal': linha_mensal, 'anual':linha_anual}
document.querySelectorAll('.adicionar').forEach(element => {
  element.addEventListener('click', function(event){
    let linha = escolha[event.target.parentElement.parentElement.id]
    adicionar_linha(event, linha)
  })
})

document.querySelectorAll('.delete').forEach(element => {
  element.addEventListener('click', function (event) {
    deletar(event)
  })
})

const enquadramentos = {
  '': [[],[]],
  'l-m': [['fiscal', 'contabil', 'sped fiscal', 'dctf', 'parcelamento', 'importação'], ['dirf', 'sped ecd', 'sped ecf']],
  'l-f': [['fiscal', 'importação'], []],
  'm': [['fiscal'], ['dasm-simei']], 
  's-m': [['fiscal', 'contabil', 'reinf', 'sintegra', 'parcelamento', 'destda', 'importação'],['dirf', 'defis', 'sped ecd']],
  's-f': [['fiscal', 'reinf', 'importação'], []],
  'p-m': [['fiscal', 'contabil', 'reinf', 'sped fiscal', 'sped contrib', 'dctf', 'parcelamento', 'importação'], ['dirf', 'sped ecd', 'sped ecf']],
  'p-f': [['fiscal', 'importação'], []],
  't': [['dctf', 'reinf', 'contabil', 'importação'],['sped ecd', 'sped ecf', 'dirf']],
}


if (document.getElementById('id_enquadramento_editavel')){
  document.getElementById('id_enquadramento_editavel').addEventListener('change', function (event) {
  enquadrar(event)
})}
