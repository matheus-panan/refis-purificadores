import pandas as pd
from datetime import datetime

def processar_relatorio_diario():
    df_diario = pd.read_excel('reldiario.xlsx')
    colunas_para_excluir = []
    if len(df_diario.columns) > 2:
        colunas_para_excluir.append(2)  
    if len(df_diario.columns) > 3:
        colunas_para_excluir.append(3)  
    if len(df_diario.columns) > 9:
        colunas_para_excluir.append(9) 
    
    df_diario = df_diario.drop(df_diario.columns[colunas_para_excluir], axis=1)
    
    novas_colunas = ['idclifor', 'nome', 'dtmovimento', 'idsubproduto', 
                     'descricaoproduto', 'qtdproduto', 'valtotliquido']
    
    if len(df_diario.columns) == 7:
        df_diario['status'] = '' 
        novas_colunas.append('status')

    novas_colunas = novas_colunas[:len(df_diario.columns)]
    df_diario.columns = novas_colunas

    ids_para_filtrar = [838, 852, 878, 880, 891, 893, 902, 13438, 16735, 17420, 19017, 21710, 23831, 30177, 
                        29138, 29140, 29142, 29144, 29168, 29170, 54735, 54935, 54937, 55158, 58214]

    if 'idsubproduto' in df_diario.columns:
        df_filtrado = df_diario[df_diario['idsubproduto'].isin(ids_para_filtrar)]
    else:
        print("AVISO: Coluna 'idsubproduto' não encontrada. Pulando filtro.")
        df_filtrado = df_diario

    if 'status' in df_filtrado.columns:
        df_filtrado['status'] = 'V'
    else:
        df_filtrado['status'] = 'V'

    df_filtrado['dtmovimento'] = pd.to_datetime(df_filtrado['dtmovimento'], format='%d/%m/%Y', errors='coerce')

    return df_filtrado

def geraRelatorioDiario(): 
    df_ultima_compra = processar_relatorio_diario()

    try:
        with pd.ExcelWriter('reldiario.xlsx', engine='openpyxl', mode='a') as writer:
            df_ultima_compra.to_excel(writer, sheet_name='ultima compra', index=False)
    except Exception as e:
        print(f"Erro ao salvar aba 'ultima compra': {e}")
    
    print("Processo concluído com sucesso!")