function copiarCoresPorID() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // Ajuste os nomes das suas planilhas aqui
  var planilhaOrigem = ss.getSheetByName('Banco de dados BI'); // Planilha com as cores
  var planilhaDestino = ss.getSheetByName('Lista Gabrielly'); // Planilha que receberá as cores
  
  // Pegar todos os dados das planilhas
  var dadosOrigem = planilhaOrigem.getDataRange();
  var dadosDestino = planilhaDestino.getDataRange();
  
  var valoresOrigem = dadosOrigem.getValues();
  var valoresDestino = dadosDestino.getValues();
  
  // Criar um mapa de ID -> cor da planilha origem
  var mapaCores = {};
  
  // Percorrer planilha origem e guardar as cores por ID
  for (var i = 1; i < valoresOrigem.length; i++) { // Começar da linha 2 (índice 1)
    var id = valoresOrigem[i][0]; // ID na coluna A
    if (id && id.toString().trim() !== '') {
      // Pegar a cor de fundo da linha inteira
      var linhaCor = planilhaOrigem.getRange(i + 1, 1, 1, valoresOrigem[i].length).getBackgrounds()[0];
      mapaCores[id] = linhaCor;
    }
  }
  
  // Aplicar as cores na planilha destino
  for (var j = 1; j < valoresDestino.length; j++) { // Começar da linha 2 (índice 1)
    var idDestino = valoresDestino[j][0]; // ID na coluna A
    
    if (idDestino && mapaCores[idDestino]) {
      // Aplicar a cor na linha inteira
      var linhaDestino = planilhaDestino.getRange(j + 1, 1, 1, valoresDestino[j].length);
      linhaDestino.setBackgrounds(mapaCores[idDestino]);
    }
  }
  
  // Mostrar mensagem de sucesso
  //SpreadsheetApp.getUi().alert('Cores copiadas com sucesso!');
}

// Versão alternativa que copia apenas a cor da primeira coluna
function copiarCoresSomenteID() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  
  var planilhaOrigem = ss.getSheetByName('Banco de dados BI');
  var planilhaDestino = ss.getSheetByName('Lista Gabrielly');
  
  var ultimaLinhaOrigem = planilhaOrigem.getLastRow();
  var ultimaLinhaDestino = planilhaDestino.getLastRow();
  
  var mapaCores = {};
  
  for (var i = 2; i <= ultimaLinhaOrigem; i++) {
    var id = planilhaOrigem.getRange(i, 1).getValue();
    var cor = planilhaOrigem.getRange(i, 1).getBackground();
    
    if (id && id.toString().trim() !== '') {
      mapaCores[id] = cor;
    }
  }
  
  // Aplicar cores na planilha destino
  for (var j = 2; j <= ultimaLinhaDestino; j++) {
    var idDestino = planilhaDestino.getRange(j, 1).getValue();
    
    if (idDestino && mapaCores[idDestino]) {
      // Aplicar cor apenas na primeira coluna
      planilhaDestino.getRange(j, 1).setBackground(mapaCores[idDestino]);
      
      // OU aplicar na linha inteira (descomente a linha abaixo)
      // planilhaDestino.getRange(j, 1, 1, planilhaDestino.getLastColumn()).setBackground(mapaCores[idDestino]);
    }
  }
  
  //SpreadsheetApp.getUi().alert('Cores aplicadas com sucesso!');
}

// Versão que copia cor da linha inteira
function copiarCoresLinhaCompleta() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  
  var planilhaOrigem = ss.getSheetByName('Banco de dados BI');
  var planilhaDestino = ss.getSheetByName('Lista Gabrielly');
  
  var ultimaLinhaOrigem = planilhaOrigem.getLastRow();
  var ultimaLinhaDestino = planilhaDestino.getLastRow();
  //var ultimaColunaOrigem = planilhaOrigem.getLastColumn();
  //var ultimaColunaDestino = planilhaDestino.getLastColumn();
  
  // Criar mapa de ID -> cores da linha
  var mapaCores = {};
  
  for (var i = 2; i <= ultimaLinhaOrigem; i++) {
    var id = planilhaOrigem.getRange(i, 1).getValue();
    
    if (id && id.toString().trim() !== '') {
      // Pegar apenas a cor da célula do ID (coluna A)
      var corID = planilhaOrigem.getRange(i, 1).getBackground();
      mapaCores[id] = corID;
    }
  }
  
  // Aplicar cores na planilha destino
  for (var j = 2; j <= ultimaLinhaDestino; j++) {
    var idDestino = planilhaDestino.getRange(j, 1).getValue();
    
    if (idDestino && mapaCores[idDestino]) {
      // Aplicar a cor apenas na célula do ID (coluna A)
      planilhaDestino.getRange(j, 1).setBackground(mapaCores[idDestino]);
    }
  }
}