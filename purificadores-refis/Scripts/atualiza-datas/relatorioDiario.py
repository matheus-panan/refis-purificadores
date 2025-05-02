import pandas as pd
#import os
from datetime import datetime

def processar_relatorio_diario():
    # 1. Carregar o arquivo reldiario.xlsx
    df_diario = pd.read_excel('reldiario.xlsx')
    
    # 2. Remover colunas C, D e J (índices 2, 3 e 9)
    # Verificar se temos colunas suficientes antes de tentar remover
    colunas_para_excluir = []
    if len(df_diario.columns) > 2:
        colunas_para_excluir.append(2)  # Coluna C
    if len(df_diario.columns) > 3:
        colunas_para_excluir.append(3)  # Coluna D
    if len(df_diario.columns) > 9:
        colunas_para_excluir.append(9)  # Coluna J
    
    df_diario = df_diario.drop(df_diario.columns[colunas_para_excluir], axis=1)
    
    # 3. Renomear as colunas - adaptamos para o número real de colunas
    novas_colunas = ['idclifor', 'nome', 'dtmovimento', 'idsubproduto', 
                     'descricaoproduto', 'qtdproduto', 'valtotliquido']
    
    # Adicionar 'status' apenas se tivermos 7 colunas (para completar 8)
    if len(df_diario.columns) == 7:
        df_diario['status'] = ''  # Criar coluna status vazia
        novas_colunas.append('status')
    
    # Ajustar os nomes das colunas conforme o número real de colunas
    novas_colunas = novas_colunas[:len(df_diario.columns)]
    df_diario.columns = novas_colunas
    
    # 4. Filtrar apenas os idsubproduto específicos
    ids_para_filtrar = [838, 852, 878, 880, 891, 893, 902, 13438, 16735, 17420, 
                        29138, 29140, 29142, 29144, 29168, 29170, 54735, 54935, 55158, 58214]
    
    # Verificar se a coluna 'idsubproduto' existe
    if 'idsubproduto' in df_diario.columns:
        df_filtrado = df_diario[df_diario['idsubproduto'].isin(ids_para_filtrar)]
    else:
        print("AVISO: Coluna 'idsubproduto' não encontrada. Pulando filtro.")
        df_filtrado = df_diario
    
    # 5. Adicionar "V" no campo status (se a coluna existir)
    if 'status' in df_filtrado.columns:
        df_filtrado['status'] = 'V'
    else:
        # Adicionar a coluna status se não existir
        df_filtrado['status'] = 'V'

    #df_filtrado['dtmovimento'] = pd.to_datetime(df_filtrado['dtmovimento'], errors='coerce')
    df_filtrado['dtmovimento'] = pd.to_datetime(df_filtrado['dtmovimento'], format='%d/%m/%Y', errors='coerce')

    return df_filtrado

def geraRelatorioDiario(): 
    # Etapa 1: Processar relatório diário
    df_ultima_compra = processar_relatorio_diario()
    
    # Salvar a aba "ultima compra" no arquivo reldiario.xlsx
    try:
        with pd.ExcelWriter('reldiario.xlsx', engine='openpyxl', mode='a') as writer:
            df_ultima_compra.to_excel(writer, sheet_name='ultima compra', index=False)
        #print("Relatório diário processado e aba 'ultima compra' salva.")
    except Exception as e:
        print(f"Erro ao salvar aba 'ultima compra': {e}")

    # Etapa 2: Atualizar o relatório final
    #df_atualizado = atualizar_relatorio_final(df_ultima_compra)
    #print(df_ultima_compra.dtypes)
    #print(df_ultima_compra)
    
    print("Processo concluído com sucesso!")