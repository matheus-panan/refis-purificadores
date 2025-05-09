import pandas as pd
from datetime import datetime

def geraRelatorioAtualizado():
    df1 = pd.read_excel("relatorio_backup.xlsx", sheet_name="backup")
    df2 = pd.read_excel("reldiario.xlsx", sheet_name="ultima compra")
    df_total = pd.concat([df1, df2], ignore_index=True)
    df_total["dtmovimento"] = pd.to_datetime(df_total["dtmovimento"], errors="coerce").dt.date
    hoje = datetime.today().date()
    df_total["diff_dias"] = (hoje - df_total["dtmovimento"]).abs()
    df_ordenado = df_total.sort_values(["idclifor", "idsubproduto", "diff_dias"])
    df_resultado = df_ordenado.drop_duplicates(subset=["idclifor", "idsubproduto"], keep="first")
    df_resultado['dtmovimento'] = pd.to_datetime(df_resultado['dtmovimento'], format='%d/%m/%Y', errors='coerce')
    df_resultado = df_resultado.drop('diff_dias', axis=1)
    df_resultado.to_excel("relatorio_atualizado.xlsx", index=False)