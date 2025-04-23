import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import time

def esperar_arquivo(caminho, timeout=300):
    """Espera até que o arquivo esteja disponível (com timeout)"""
    start_time = time.time()
    while not os.path.exists(caminho):
        if time.time() - start_time > timeout:
            raise FileNotFoundError(f"Timeout esperando pelo arquivo {caminho}")
        time.sleep(5)
    return True

def processar_relatorio_diario():
    # Caminho do arquivo que será exportado manualmente
    caminho_reldiario = 'C:/caminho/para/reldiario.xlsx'
    
    # Esperar até que o arquivo esteja disponível (máximo 5 minutos)
    print("Aguardando exportação do arquivo reldiario.xlsx...")
    esperar_arquivo(caminho_reldiario)
    print("Arquivo reldiario.xlsx encontrado!")
    
    # Carregar o arquivo Excel
    df = pd.read_excel(caminho_reldiario)
    
    # Excluir colunas C, D e J (índices 2, 3 e 9)
    colunas_para_excluir = [2, 3, 9]
    df = df.drop(df.columns[colunas_para_excluir], axis=1)
    
    # Renomear as colunas
    novas_colunas = ['idclifor', 'nome', 'dtmovimento', 'idsubproduto', 
                     'descricaoproduto', 'qtdproduto', 'valtotliquido', 'status']
    df.columns = novas_colunas
    
    # Filtrar por idsubproduto específicos
    ids_produtos = [838, 852, 878, 880, 891, 893, 902, 16735, 17420, 
                   29138, 29140, 29142, 29144, 29168, 29170, 54935, 55158, 58214]
    df_filtrado = df[df['idsubproduto'].isin(ids_produtos)]
    
    # Preencher a coluna status com 'V'
    df_filtrado['status'] = 'V'
    
    # Criar uma aba "ultima compra" no mesmo arquivo
    with pd.ExcelWriter(caminho_reldiario, engine='openpyxl', mode='a') as writer:
        df_filtrado.to_excel(writer, sheet_name='ultima compra', index=False)
    
    return df_filtrado

def atualizar_relatorio_final(df_ultima_compra):
    # Carregar o relatório final
    caminho_relatorio_final = 'C:/caminho/para/relatorio_final.xlsx'
    df_final = pd.read_excel(caminho_relatorio_final)
    
    # Garantir que datas estejam no formato correto
    df_ultima_compra['dtmovimento'] = pd.to_datetime(df_ultima_compra['dtmovimento'])
    df_final['dtmovimento'] = pd.to_datetime(df_final['dtmovimento'])
    
    # Para cada cliente no relatório diário
    for _, row in df_ultima_compra.iterrows():
        cliente_id = row['idclifor']
        
        # Verificar se o cliente já existe no relatório final
        cliente_existente = df_final[df_final['idclifor'] == cliente_id]
        
        if len(cliente_existente) > 0:
            # Cliente existe, verificar data mais recente
            idx = cliente_existente.index[0]
            if row['dtmovimento'] > df_final.loc[idx, 'dtmovimento']:
                # Atualizar dados com informações mais recentes
                for coluna in df_final.columns:
                    df_final.loc[idx, coluna] = row[coluna]
        else:
            # Cliente não existe, adicionar ao dataframe
            df_final = pd.concat([df_final, pd.DataFrame([row])], ignore_index=True)
    
    # Salvar o relatório final atualizado
    df_final.to_excel(caminho_relatorio_final, index=False)
    
    return df_final

def atualizar_google_sheets(df_final):
    # Configurar acesso ao Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name('caminho/para/credenciais.json', scope)
    client = gspread.authorize(credentials)
    
    # Abrir a planilha do Google Sheets
    planilha = client.open("Nome_Da_Sua_Planilha_No_Google")
    worksheet = planilha.worksheet("Nome_Da_Aba")
    
    # Limpar a planilha existente
    worksheet.clear()
    
    # Adicionar cabeçalhos
    worksheet.update('A1', [df_final.columns.tolist()])
    
    # Adicionar dados
    worksheet.update('A2', df_final.values.tolist())
    
    print("Google Sheets atualizado com sucesso!")

def executar_fluxo_completo():
    print("Iniciando processo de automação...")
    
    # Etapa 1: Processar o relatório diário
    df_ultima_compra = processar_relatorio_diario()
    print("Processamento do relatório diário concluído!")
    
    # Etapa 2: Atualizar o relatório final
    df_final = atualizar_relatorio_final(df_ultima_compra)
    print("Relatório final atualizado!")
    
    # Etapa 3: Atualizar o Google Sheets
    atualizar_google_sheets(df_final)
    print("Processo completo finalizado com sucesso!")

if __name__ == "__main__":
    executar_fluxo_completo()