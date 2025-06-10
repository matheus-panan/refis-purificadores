function calculateScores() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var lastRow = sheet.getLastRow();
  var data = sheet.getDataRange().getValues();
  var ids = sheet.getRange("A2:A" + sheet.getLastRow()).getValues();
  sheet.getRange(2, 13, sheet.getLastRow() - 1, 1).clearContent();
  var clientesBons = []
  var clientesMedios = []
  var clientesRuins = []
  //var base_repetidos = calculaRepetidos(ids)
  var backgrounds = [];

  /* 3. Verifica a quantidade de repetições de idclifor presentes na base de dados e atribui valores ao score
        de acordo com a quantidade de repetições
  for (var j = 1; j < base_repetidos.length; j++) {
    var id = base_repetidos[j][0]; // The ID
    var count = base_repetidos[j][1]; // The occurrence count
    var score = 10;
    if (count == 2)
      score += 2;
    else if (count > 2 && count <= 4)
      score += 10;
    else if (count > 4)
      score += 20;
    else
      score += 0;
    idToScore[id] = score; // Map the ID to its calculated score
  }
  var idToScore = {};*/

  var scores = [];
  var backgrounds = [];
  // Loop principal - agora usando o score base das repetições
  for (var i = 1; i < lastRow; i++) {
    var idclifor = data[i][0]
    var notas = data[i][7]
    var status_ultimaligacao = data[i][9]; // Coluna G
    var diasSemCompra = data[i][3];
    var status = data[i][6];
    var score = 10
    
    // CORREÇÃO: Inicializa score com o valor das repetições, ou 10 se não existir
    //var score = idToScore[idclifor] || 10;
    
    // Status da última ligação
    if (status_ultimaligacao == "Venda") score += 15;
    else if (status_ultimaligacao == "Caixa postal" || status_ultimaligacao == "Não atende") score -= 5;
    else if (status_ultimaligacao == "Número incorreto") score -= 10;
    else if (status_ultimaligacao == "Não ligar mais") score -= 20;
    else if (status_ultimaligacao === "") score += 0;
    else score -= 5;

    // Status do cliente e dias sem compra
    if (status == "Ligar" && diasSemCompra > 269 && diasSemCompra < 540) score += 25;
    else if (status == "Aguardar") score += 10;
    else if (diasSemCompra >= 540 && score <= 730) score -= 5;
    else if (diasSemCompra > 730 && score <= 1095) score -= 10;
    else if (diasSemCompra > 1095 && score <= 1460) score -= 15
    else score -=20

    // Notas
    if (notas > 1 && diasSemCompra < 270) score += 2 * notas;
    else if (notas > 1 && diasSemCompra < 730) score += notas;
    else if(notas > 3) score += 1.5 * notas;

    // Normalizar score (0 a 100)
    score = Math.max(0, Math.min(100, score));

    var bgColor;
    // Classificação
    if (score > 35) {clientesBons.push(idclifor);bgColor = "#b7e1cd";}
    else if (score > 5 && score <=35) {clientesMedios.push(idclifor); bgColor = "#fff2cc";}
    else {clientesRuins.push(idclifor);bgColor = "#f4c7c3";}

    scores.push([score]);
    backgrounds.push([bgColor]);
    //sheet.getRange(i + 1, 12).setValue(score);
  }
  if (scores.length > 0) {
    var range = sheet.getRange(2, 12, scores.length, 1);
    var range2 = sheet.getRange(2, 1, scores.length, 1);
    range.setValues(scores);
    range2.setBackgrounds(backgrounds);
  }
  //return clientesBons
  //return separaClientes(clientesBons, clientesMedios, clientesRuins)
}/*

function calculaRepetidos(ids) {
  // Step 1: Count occurrences of each ID
  var contagem = {};
  ids.forEach(function(id) {
    if (id[0]) { // Check if ID is non-empty (ids is 2D array, so use id[0])
      contagem[id[0]] = (contagem[id[0]] || 0) + 1;
    }
  });
  // Step 2: Create result array with same length as input
  var resultados = [["ID", "Quantidade de Repetições"]];
  for (var i = 0; i < ids.length; i++) {
    var id = ids[i][0];
    if (id) { // Only include non-empty IDs
      resultados.push([id, contagem[id] || 1]); // Use count from contagem, default to 1 if not found
    }
  }
  if (resultados.length === 1) // Only header, no valid IDs
    return;
  return resultados;
}
function calculateScores() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var lastRow = sheet.getLastRow();
  var data = sheet.getDataRange().getValues();
  var ids = sheet.getRange("A2:A" + sheet.getLastRow()).getValues();
  
  // Limpa conteúdo e formatação da coluna de scores (coluna 12)
  sheet.getRange(2, 12, sheet.getLastRow() - 1, 1).clearContent().clearFormat();
  
  var clientesBons = [];
  var clientesMedios = [];
  var clientesRuins = [];
  
  // Preparar arrays para scores e cores
  var scores = [];
  var backgrounds = [];
  
  // Loop principal
  for (var i = 1; i < lastRow; i++) {
    var idclifor = data[i][0];
    var notas = data[i][7];
    var status_ultimaligacao = data[i][9];
    var diasSemCompra = data[i][3];
    var status = data[i][6];
    var score = 10;
    
    // Sua lógica de cálculo de score permanece a mesma
    if (status_ultimaligacao == "Venda") score += 15;
    else if (status_ultimaligacao == "Caixa postal" || status_ultimaligacao == "Não atende") score -= 5;
    else if (status_ultimaligacao == "Número incorreto") score -= 10;
    else if (status_ultimaligacao == "Não ligar mais") score -= 20;
    else if (status_ultimaligacao === "") score += 0;
    else score -= 5;

    if (status == "Ligar" && diasSemCompra > 269 && diasSemCompra < 540) score += 25;
    else if (status == "Aguardar") score += 10;
    else if (diasSemCompra >= 540 && diasSemCompra <= 730) score -= 5;
    else if (diasSemCompra > 730 && diasSemCompra <= 1095) score -= 10;
    else if (diasSemCompra > 1095 && diasSemCompra <= 1460) score -= 15;
    else if (diasSemCompra > 1460) score -= 20;

    if (notas > 1 && diasSemCompra < 270) score += 2 * notas;
    else if (notas > 1 && diasSemCompra < 730) score += notas;
    else if(notas > 3) score += 1.5 * notas;

    score = Math.max(0, Math.min(100, score));

    // Classificação e definição de cor
    var bgColor;
    if (score > 35) {
      clientesBons.push(idclifor);
      bgColor = "#b7e1cd"; // Verde claro
    } else if (score > 5 && score <=35) {
      clientesMedios.push(idclifor);
      bgColor = "#fff2cc"; // Amarelo claro
    } else {
      clientesRuins.push(idclifor);
      bgColor = "#f4c7c3"; // Vermelho claro
    }
    
    scores.push([score]);
    backgrounds.push([bgColor]);
  }
  
  // Aplica todos os scores e cores de uma vez (mais eficiente)
  if (scores.length > 0) {
    var range = sheet.getRange(2, 12, scores.length, 1);
    var range2 = sheet.getRange(2, 1, scores.length, 1);
    range.setValues(scores);
    range2.setBackgrounds(backgrounds);
  }
  
  console.log("Clientes bons: "+ clientesBons.length +"\nClientes médios: "+ clientesMedios.length +"\nClientes Ruins: "+ clientesRuins.length);

  return clientesBons;
}*/