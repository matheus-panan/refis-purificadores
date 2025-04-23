"""import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
import os.path

# Carrega as duas abas do Excel
df_RelatorioFinal = pd.read_excel("resultado_final.xlsx", sheet_name="Sheet1")
df_RelatorioDiario = pd.read_excel("reldiario.xlsx", sheet_name="ultima compra")

# Junta os dois dataframes
df_total = pd.concat([df_RelatorioFinal, df_RelatorioDiario], ignore_index=True)

# Converte coluna de data para datetime e extrai apenas a parte da data (sem hora)
df_total["dtmovimento"] = pd.to_datetime(df_total["dtmovimento"], errors="coerce").dt.date

# Obtém a data de hoje (apenas data, sem hora)
hoje = datetime.today()

# Calcula a diferença em dias (valor absoluto)
#df_total["diff_dias"] = (hoje - df_total["dtmovimento"]).abs()

#df_total["dtmovimento"] = pd.to_datetime(df_total["dtmovimento"], unit='D', origin='1899-12-30').dt.date

df_total["dtmovimento"] = pd.to_numeric(df_total["dtmovimento"], errors='coerce')

# Passo 2: Converter datas Excel
df_total["dtmovimento"] = pd.to_datetime(
    df_total["dtmovimento"],
    unit='D',
    origin='1899-12-30',
    errors='coerce'
).dt.date

# Ordena por idclifor, codproduto e diferença de dias (menor primeiro = mais recente)
df_ordenado = df_total.sort_values(["idclifor", "idsubproduto", "diff_dias"])

# Remove duplicatas mantendo a combinação mais recente de cliente+produto
df_resultado = df_ordenado.drop_duplicates(subset=["idclifor", "idsubproduto"], keep="first")

# Salva o resultado
with pd.ExcelWriter('resultado_final.xlsx', engine='openpyxl', mode='a') as writer:
  df_resultado.to_excel(writer, sheet_name='base atualizada2', index=False)
"""            
import pandas as pd
from datetime import datetime

# Carrega as duas abas do Excel
df1 = pd.read_excel("resultado_final.xlsx", sheet_name="Sheet1")
df2 = pd.read_excel("reldiario.xlsx", sheet_name="ultima compra")

# Junta os dois dataframes
df_total = pd.concat([df1, df2], ignore_index=True)

# Converte coluna de data para datetime e extrai apenas a parte da data (sem hora)
df_total["dtmovimento"] = pd.to_datetime(df_total["dtmovimento"], errors="coerce").dt.date

# Obtém a data de hoje (apenas data, sem hora)
hoje = datetime.today().date()

# Calcula a diferença em dias (valor absoluto)
df_total["diff_dias"] = (hoje - df_total["dtmovimento"]).abs()

# Ordena por idclifor, codproduto e diferença de dias (menor primeiro = mais recente)
df_ordenado = df_total.sort_values(["idclifor", "idsubproduto", "diff_dias"])

# Remove duplicatas mantendo a combinação mais recente de cliente+produto
df_resultado = df_ordenado.drop_duplicates(subset=["idclifor", "idsubproduto"], keep="first")

# Salva o resultado
df_resultado.to_excel("resultado_att.xlsx", index=False)
