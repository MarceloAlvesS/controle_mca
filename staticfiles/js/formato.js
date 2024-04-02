function atualizar_tabela(event) {
  if (event){
  event.preventDefault()
  }
  document.getElementById(conversao[formato.value][0]).style.display = 'none'
  document.getElementById(conversao[formato.value][1]).style.display = ''
}

const conversao = {'M': ['anual', 'mensal'], 'A': ['mensal', 'anual']}

const formato = document.getElementById('id_formato')
formato.addEventListener('change', function(event) {
  atualizar_tabela(event)
})
evento = new Event('change')
formato.dispatchEvent(evento)


function apagar_remanescente() {
  let remanescente = conversao[formato.value][0]
  document.getElementById('tabelas').removeChild(document.getElementById(remanescente))
}


const submit = document.getElementById('buttom_submit')
submit.addEventListener('click', function (event) {
  event.preventDefault()
  apagar_remanescente()
  document.getElementById('formulario').submit()
})
