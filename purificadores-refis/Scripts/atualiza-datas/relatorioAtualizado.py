import pandas as pd
from datetime import datetime

# Carrega as duas abas do Excel
df1 = pd.read_excel("relatorio_backup.xlsx", sheet_name="backup")
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
df_resultado['dtmovimento'] = pd.to_datetime(df_resultado['dtmovimento'], format='%d/%m/%Y', errors='coerce')
#print(df_resultado.dtypes)

df_resultado = df_resultado.drop('diff_dias', axis=1)

# Salva o resultado
df_resultado.to_excel("relatorio_atualizado.xlsx", index=False)