function atualizarDatas() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var planilhaAtual = ss.getSheetByName("Última Compra"); // nome da sua planilha
  //var relatorio = ss.getSheetByName("Relatório"); // vai pegar o arquivo XLS do ciss
  
  // Passo 2. Fazer o upload do arquivo no google drive

  // Obter dados
  var dadosAtuais = planilhaAtual.getDataRange().getValues();
  var dadosRelatorio = relatorio.getDataRange().getValues();
  
  // Criar mapa do relatório (ID -> Data)
  var mapaRelatorio = {};
  for (var i = 1; i < dadosRelatorio.length; i++) {
    var id = dadosRelatorio[i][0]; // assumindo que ID está na coluna A
    var data = dadosRelatorio[i][1]; // data na coluna B
    mapaRelatorio[id] = data;
  }
  
  // Atualizar planilha
  for (var j = 1; j < dadosAtuais.length; j++) {
    var idAtual = dadosAtuais[j][0];
    var dataAtual = dadosAtuais[j][1];
    var dataRelatorio = mapaRelatorio[idAtual];
    
    if (dataRelatorio && dataRelatorio > dataAtual) {
      planilhaAtual.getRange(j+1, 2).setValue(dataRelatorio); // atualiza coluna B
    }
  }
  SpreadsheetApp.getUi().alert('Atualização concluída!');
}