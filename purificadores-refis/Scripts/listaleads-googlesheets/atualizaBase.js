function atualizarBaseDeDadosComHistorico() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const historicoSheet = ss.getSheetByName("Historico ligações");
  const baseSheet = ss.getSheetByName("Base de dados BI");

  baseSheet.getRange(2, 9, baseSheet.getLastRow() - 1, 3).clearContent();

  const historico = historicoSheet.getDataRange().getValues();
  const base = baseSheet.getDataRange().getValues();

  // Cria mapa com dados do histórico mais recentes por idclifor
  const historicoMap = new Map();

  for (let i = 1; i < historico.length; i++) {
    const id = historico[i][0];
    const status = historico[i][2];         
    const dataLigacao = historico[i][3];    
    const observacao = historico[i][4];     

    if (!(dataLigacao instanceof Date)) continue;

    if (!historicoMap.has(id) || historicoMap.get(id).dataLigacao < dataLigacao) {
      historicoMap.set(id, { status, dataLigacao, observacao });
    }
  }

  // Cria mapa para identificar duplicatas de idclifor na base
  const idCountMap = new Map();
  for (let i = 1; i < base.length; i++) {
    const idBase = base[i][0];
    idCountMap.set(idBase, (idCountMap.get(idBase) || 0) + 1);
  }

  // Organiza os registros da base por idclifor
  const registrosPorId = new Map();
  for (let i = 1; i < base.length; i++) {
    const idBase = base[i][0];
    if (!registrosPorId.has(idBase)) {
      registrosPorId.set(idBase, []);
    }
    registrosPorId.get(idBase).push({ rowIndex: i, status: base[i][6] });
  }

  // Para ids duplicados, verifica se há pelo menos um "Aguardar"
  registrosPorId.forEach((registros, idBase) => {
    if (registros.length > 1) {
      const temAguardar = registros.some(r => r.status === "Aguardar");
      if (temAguardar) {
        registros.forEach(r => {
          if (r.status === "Ligar") {
            baseSheet.getRange(r.rowIndex + 1, 7).setValue("Não ligar");
          }
        });
      }
    }
  });

  // Atualiza os dados da base
  for (let i = 1; i < base.length; i++) {
    const idBase = base[i][0];
    const dataBase = base[i][8];

    // Atualiza dados do histórico se existir
    if (historicoMap.has(idBase)) {
      const { status, dataLigacao, observacao } = historicoMap.get(idBase);
      const deveAtualizar = !(dataBase instanceof Date) || dataLigacao > dataBase;

      if (deveAtualizar) {
        baseSheet.getRange(i + 1, 9).setValue(dataLigacao);
        baseSheet.getRange(i + 1, 10).setValue(status);
        baseSheet.getRange(i + 1, 11).setValue(observacao);
      }
    }
  }
  //alteraStatus()
  calculateScores()
  //return calculateScores()
  Logger.log("Base de dados atualizada com os dados mais recentes do histórico.");
}

function alteraStatus(){
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const baseSheet = ss.getSheetByName("Base de dados BI");
  const base = baseSheet.getDataRange().getValues();
  for (let i = 1; i < base.length; i++) {
    const statusUltimaLigacao = base[i][9]; // Coluna I (status_ultimaligacao)
    if (statusUltimaLigacao === "Não ligar mais")
      baseSheet.getRange(i + 1, 7).setValue("Não ligar");
  }

}