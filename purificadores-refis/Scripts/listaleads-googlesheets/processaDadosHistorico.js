function copiarHistorico(origemUrl, origemNomeAba, destinoNomeAba) {
  var hoje = new Date();
  if (hoje.getDay() === 0) // Hoje é domingo. A função não será executada
    return;
  
  var destinoUrl = "https://docs.google.com/spreadsheets/d/1DQAUJlgrTerE_zJ9e7e1boT32n18ZYdZaqKfuC0ZUFI/edit";
  var origemIntervalo = "A2:F41";
  var origemPlanilha = SpreadsheetApp.openByUrl(origemUrl);
  var destinoPlanilha = SpreadsheetApp.openByUrl(destinoUrl);
  var origemAba = origemPlanilha.getSheetByName(origemNomeAba);
  var destinoAba = destinoPlanilha.getSheetByName(destinoNomeAba);
  var dados = origemAba.getRange(origemIntervalo).getValues();
  
  var fusoHorario = "GMT-4";
  var dataFormatada = Utilities.formatDate(new Date(), fusoHorario, "dd-MM-yyyy");

  var dadosComData = dados.map(function(linha) {
    return [              
      linha[0],          
      linha[1],          
      linha[4],
      dataFormatada,          
      linha[5]           
    ];
  });
  
  // Encontrar a última linha com conteúdo
  var ultimaLinha = destinoAba.getLastRow();
  
  // Se a planilha estiver vazia, começa na linha 1
  var linhaInserir = ultimaLinha === 0 ? 1 : ultimaLinha + 1;
  
  // Inserir os dados
  destinoAba.getRange(linhaInserir, 1, dadosComData.length, dadosComData[0].length)
    .setValues(dadosComData);
  
  var totalLinhas = destinoAba.getLastRow();
  if (totalLinhas > 1) { // Só ordenar se houver mais de uma linha
    var intervaloOrdenacao = destinoAba.getRange(1, 1, totalLinhas, destinoAba.getLastColumn());
    intervaloOrdenacao.sort({column: 4, ascending: false}); // Coluna 4, ordem decrescente
  }
}