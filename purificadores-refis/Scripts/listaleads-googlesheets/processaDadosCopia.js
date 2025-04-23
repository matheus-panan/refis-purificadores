/*  Função genérica que copia dados da lista geradas na planilha "Banco de dados" e cola em outras planilhas. 
    O que define para onde estes dados serão colados é o nome da aba da planilha de origem e o URL da planilha de destino
*/

function copiarParaLista(nomeLista, urlDestino) {
  try {
    // 1. Acessar a planilha e aba de origem
    var origem = SpreadsheetApp.getActiveSpreadsheet();
    var sheetOrigem = origem.getSheetByName(nomeLista);
    
    // 2. Acessar a planilha de destino
    var destino = SpreadsheetApp.openByUrl(urlDestino);
    
    // 3. Obter ou criar a aba de destino
    var sheetDestino = destino.getSheetByName(nomeLista) || destino.insertSheet(nomeLista);

    // 4. Obter dados da origem
    sheetDestino.getRange("A2:D41").clearContent();
    
    // 5. Obter dados da origem
    var dados = sheetOrigem.getDataRange().getValues();
    
    validarPlanilhas(sheetOrigem, destino, dados)

    // Se a planilha estiver completamente vazia, ultimaLinha será 0
    var linhaInicio = 1;
    
    // 6. Colar os dados
    sheetDestino.getRange(linhaInicio, 1, dados.length, dados[0].length).setValues(dados);
    
  } catch (error) {
    console.error("Erro: " + error.message);
    SpreadsheetApp.getUi().alert("Erro: " + error.message);
  }
}

// Valida se as planilhas de destino e origem existem, e se têm dados para serem copiados
function validarPlanilhas(sheetOrigem, destino, dados){
  if (!sheetOrigem)
      throw new Error("A aba não foi encontrada na planilha de origem");
  if (!destino)
      throw new Error("Não foi possível acessar a planilha de destino");
  if (dados.length === 0)
      throw new Error("Nenhum dado encontrado na planilha de origem");
}