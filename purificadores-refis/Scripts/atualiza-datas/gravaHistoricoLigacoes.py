import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def gravaHistorico():
  SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
  SAMPLE_SPREADSHEET_ID1 = "153BTT_4N4A9XEIml2NLNN6jb0QqI4KgW_hGTyzqLWZ0"
  SAMPLE_SPREADSHEET_ID2 = "1SGzQA62IQVkjwD0fmejLsLMHoKz53B77J-8xCu7jIgw"
  SAMPLE_RANGE_NAME1 = "Lista Gabrielly!A2:E41"
  SAMPLE_RANGE_NAME2 = "Lista Maria!A2:E41"
                       
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
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID1, range=SAMPLE_RANGE_NAME1).execute()  
    # Extrair os dados da chave 'values'
    values = result.get('values', [])
    if not values:
        print("Nenhum dado encontrado na planilha.")
        return
    # A primeira linha contém os cabeçalhos
    #headers = values[0]
        # As demais linhas são os dados (a partir da segunda linha)
    data = values[1:]

    # Criar um DataFrame com os dados
    df = pd.DataFrame(data)

    # Remover linhas completamente vazias
    df = df.dropna(how='all')

    # Renomear as colunas para corresponder ao padrão da imagem (se necessário)
    df.columns = ['idclifor', 'nome', 'tentativa1', 'tentativa2', 'dtmovimento']
    df['idclifor'] = pd.to_numeric(df['idclifor'], errors='coerce', downcast='integer')

    # dtmovimento: Data (formato DD/MM/YYYY)
    #df['dtmovimento'] = pd.to_datetime(df['dtmovimento'], format='%d/%m/%Y', errors='coerce')
    #pd.to_datetime(df['dtmovimento'], format='%d/%m/%Y', errors='coerce')
    #df.to_excel("historicos.xlsx", index=False)

    with pd.ExcelWriter('historicos.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='Gabrielly', index=False)


    # Ler os valores da planilha
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID2, range=SAMPLE_RANGE_NAME2).execute()  
    # Extrair os dados da chave 'values'
    values = result.get('values', [])
    if not values:
        print("Nenhum dado encontrado na planilha.")
        return
    # A primeira linha contém os cabeçalhos
    #headers = values[0]
        # As demais linhas são os dados (a partir da segunda linha)
    data = values[1:]

    # Criar um DataFrame com os dados
    df = pd.DataFrame(data)

    # Remover linhas completamente vazias
    df = df.dropna(how='all')

    # Renomear as colunas para corresponder ao padrão da imagem (se necessário)
    df.columns = ['idclifor', 'nome', 'tentativa1', 'tentativa2', 'dtmovimento']
    df['idclifor'] = pd.to_numeric(df['idclifor'], errors='coerce', downcast='integer')

    # dtmovimento: Data (formato DD/MM/YYYY)
    #df['dtmovimento'] = pd.to_datetime(df['dtmovimento'], format='%d/%m/%Y', errors='coerce')
    #pd.to_datetime(df['dtmovimento'], format='%d/%m/%Y', errors='coerce')
    #df.to_excel("historicos.xlsx", index=False)
    
    with pd.ExcelWriter('historicos.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='Maria', index=False)

  except HttpError as err:
    print("erro:" + err)
