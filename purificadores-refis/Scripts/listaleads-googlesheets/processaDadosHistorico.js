function copiarHistorico(origemUrl, origemNomeAba, destinoNomeAba) {
  var hoje = new Date();
  if (hoje.getDay() === 0) //Hoje é domingo. A função não será executada
        return;
  else { 
    var destinoUrl = "https://docs.google.com/spreadsheets/d/1DQAUJlgrTerE_zJ9e7e1boT32n18ZYdZaqKfuC0ZUFI/edit"
    var origemIntervalo = "A2:D41";
    var origemPlanilha = SpreadsheetApp.openByUrl(origemUrl);
    var destinoPlanilha = SpreadsheetApp.openByUrl(destinoUrl);
    var origemAba = origemPlanilha.getSheetByName(origemNomeAba);
    var destinoAba = destinoPlanilha.getSheetByName(destinoNomeAba);
    var dados = origemAba.getRange(origemIntervalo).getValues();
    var ultimaLinha = destinoAba.getRange("A:A").getValues().filter(String).length;
    var linhaData = ultimaLinha + 1;
    var dataAtual = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "dd/MM/yyyy");
    destinoAba.getRange(linhaData, 1).setValue(dataAtual);
    destinoAba.getRange(linhaData, 1)
      .setFontWeight("bold")
      .setHorizontalAlignment("center");
    var linhaDados = linhaData + 1;
    destinoAba.getRange(linhaDados, 1, dados.length, dados[0].length).setValues(dados);
  }
}