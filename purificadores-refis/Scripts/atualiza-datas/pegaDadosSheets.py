import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1DQAUJlgrTerE_zJ9e7e1boT32n18ZYdZaqKfuC0ZUFI"
SAMPLE_RANGE_NAME = "Última Compra!A:H"

def main():
  
  creds = None
  
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Conectar à API do Google Sheets
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # Ler os valores da planilha
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        
    # Extrair os dados da chave 'values'
    values = result.get('values', [])
    if not values:
        print("Nenhum dado encontrado na planilha.")
        return

    # A primeira linha contém os cabeçalhos
    headers = values[0]
    # As demais linhas são os dados (a partir da segunda linha)
    data = values[1:]

    # Criar um DataFrame com os dados
    df = pd.DataFrame(data)

    # Remover linhas completamente vazias
    df = df.dropna(how='all')

    # Renomear as colunas para corresponder ao padrão da imagem (se necessário)
    df.columns = ['idclifor', 'nome', 'dtmovimento', 'idsubproduto', 'descricaoproduto', 'qtdproduto', 'valtotliquido', 'status']

    # Converter os tipos de dados
    # idclifor: Inteiro
    df['idclifor'] = pd.to_numeric(df['idclifor'], errors='coerce', downcast='integer')

    # nome: String (já está como string, não precisa de conversão)

    # dtmovimento: Data (formato DD/MM/YYYY)
    df['dtmovimento'] = pd.to_datetime(df['dtmovimento'], format='%d/%m/%Y', errors='coerce')
    #pd.to_datetime(df['dtmovimento'], format='%d/%m/%Y', errors='coerce')
    

    # idsubproduto: Inteiro
    df['idsubproduto'] = pd.to_numeric(df['idsubproduto'], errors='coerce', downcast='integer')

    # descricaoproduto: String (já está como string)

    # qtdproduto: Inteiro
    df['qtdproduto'] = pd.to_numeric(df['qtdproduto'], errors='coerce', downcast='integer')

    # valtotliquido: Float (considerando vírgula como separador decimal)
    df['valtotliquido'] = df['valtotliquido'].str.replace(',', '.', regex=False)  # Substituir vírgula por ponto
    df['valtotliquido'] = pd.to_numeric(df['valtotliquido'], errors='coerce')    
    print(df.dtypes)
    #print(df['dtmovimento'])
    # Exportar para Excel
    #output_file = "teste.xlsx"
    with pd.ExcelWriter('relatorio_backup.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='backup', index=False)
    #print(f"Dados exportados com sucesso para {output_file}")
    
  except HttpError as err:
    print(err)

if __name__ == "__main__":
  main()
