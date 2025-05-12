function inicializarPlanilhas() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  return {
    dadosSheet: ss.getSheetByName("Última Compra"),
    listaMariaSheet: ss.getSheetByName("Lista Maria"),
    listaGabriellySheet: ss.getSheetByName("Lista Gabrielly")
  };
}

function obterDadosPlanilha(dadosSheet){
  // Obtendo os dados da aba "Ultima Compra"
  var dataRange = dadosSheet.getDataRange();
  var data = dataRange.getValues();
  return data
}

function limpaPlanilhas(listaMariaSheet, listaGabriellySheet){
  // Limpa as listas anteriores
  listaMariaSheet.getRange("A2:A41").clearContent();
  listaGabriellySheet.getRange("A2:A41").clearContent();
}

function obterDataLimite(){
  // Obtendo a data de 9 meses atrás
  var dataUltimaCompra = new Date();
  dataUltimaCompra.setMonth(dataUltimaCompra.getMonth() - 9);
  return dataUltimaCompra
}

function criarListaClientesValidos(data, dataUltimaCompra, dadosSheet){
  var clientesValidos = []
  for (let i = 1; i < data.length; i++) {
    var cliente = data[i][0]; // Coluna A (Cliente)
    var status = data[i][7]; // Coluna H (Status)
    var dataCompra = new Date(data[i][2]); // Coluna C (Data da Última Compra)
    
    /* Verifica se a compra é anterior a 9 meses e se o status não é 'V' (Isso existe para casos em que o cliente nao comprou
     mas já foi verificado que não é possível realizar a troca do refil por qualquer motivo que seja)*/
    if (dataCompra < dataUltimaCompra && status !== "V")
      clientesValidos.push(cliente); // Adiciona cliente à lista de válidos
    if (dataCompra < dataUltimaCompra) {
      if (status === "V") 
        dadosSheet.getRange(i + 1, 8).setValue(""); // Coluna H (Status)
      else
        clientesValidos.push(cliente); // Adiciona cliente à lista de válidos
    }
    /*if(clientesValidos.length == 80)
      break*/
  }
  return clientesValidos
}

function processarListas(listaGabrielly, listaMaria, data, dadosSheet, listaGabriellySheet, listaMariaSheet) {
  // Combina as duas listas em um único array de objetos com a lista e sua sheet correspondente
  const listasParaProcessar = [
    { lista: listaGabrielly, sheet: listaGabriellySheet },
    { lista: listaMaria, sheet: listaMariaSheet }
  ];

  // Processa todas as listas em um único laço
  for (const { lista, sheet } of listasParaProcessar) {
    for (let j = 0; j < lista.length; j++) {
      const index = data.findIndex(row => row[0] === lista[j]);
      if (index !== -1) {
        dadosSheet.getRange(index + 1, 8); // Coluna H
      }
      sheet.getRange(j + 2, 1).setValue(lista[j]);
    }
  }
}

// Função para embaralhar um array
function embaralharArray(array) {
  for (var i = array.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1)); // Gera um índice aleatório
    // Troca elementos
    var temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
  return array;
}