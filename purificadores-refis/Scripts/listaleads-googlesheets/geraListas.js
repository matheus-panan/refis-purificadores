/*  Esta é a função principal que gera 80 clientes válidos a partir da base de dados da planilha "Banco de dados" na página   
    "Última Compra", e distribui 40 clientes para cada funcionária. 
    
    OBS1: Estes clientes para serem válidos eles devem: ter um status marcado com "V" e o intervalo da data da compra e 
    a data limite da troca do refil deve ser igual ou maior que 9 meses. 
    Se o cliente não for válido ele não entrará na lista de novos clientes gerados.

    OBS2: Para funcionar efetivamente o script, ao finalizar as vendas do dia deve-se atualizar a data da última compra e remover o "V" do status de todos clientes no qual não foram vendidos o refil.
    
    OBS3: Todas as funções que são chamadas nesta função estão no arquivo processaDadosPlanilha.gs
*/

function gerarListasClientes() {
  const {dadosSheet, listaMariaSheet, listaGabriellySheet} = inicializarPlanilhas()
  limpaPlanilhas(listaMariaSheet, listaGabriellySheet)
  var data = obterDadosPlanilha(dadosSheet)
  var clientesValidos = embaralharArray(criarListaClientesValidos(data));
  
  // Divide os clientes válidos entre as listas de Maria e Gabrielly
  var listaMaria = clientesValidos.slice(0, 40); // Pega os primeiros 40
  var listaGabrielly = clientesValidos.slice(40, 80); // Pega os próximos 40
  processarListas(listaGabrielly, listaMaria, data, dadosSheet, listaGabriellySheet, listaMariaSheet)
}