import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_credentials():
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
    return creds

def excel_to_google_sheets(excel_file, sheet_name, spreadsheet_id, range_name):
    # Ler o arquivo Excel
    df = pd.read_excel(excel_file)

    """# Tratar colunas datetime
    for col in df.select_dtypes(include=["datetime", "datetimetz"]):
        df[col] = df[col].astype(str)

    # Substituir valores nulos
    df = df.fillna("")

    # (Opcional) converter todo o DataFrame para string
    df = df.astype(str)

    # Preparar os dados para envio
    values = [df.columns.tolist()]
    values.extend(df.values.tolist())"""
    

    # Tratar colunas datetime para string
    for col in df.select_dtypes(include=["datetime", "datetimetz"]):
        if col != "dtmovimento":
            df[col] = df[col].astype(str)

    # Substituir NaNs por string vazia, exceto na coluna 'valtotliquido'
    for col in df.columns:
        #if col != "valtotliquido":
        df[col] = df[col].fillna("")
        """else:
            df[col] = df[col].fillna(0)  # ou algum outro valor padrão"""
    # Converter todas as colunas (exceto 'valtotliquido') para string
    for col in df.columns:
        if col != "valtotliquido" and "dtmovimento"and "qtdproduto"and "idsubproduto"and "idclifor":
            df[col] = df[col].astype(str)
    
    """if "valtotliquido" in df.columns:
        df["valtotliquido"] = (
        df["valtotliquido"]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )"""
        
    #df["valtotliquido"] = pd.to_numeric(df["valtotliquido"], errors="coerce").fillna(0)
        
    if('diff_dias' in df.columns):
        df = df.drop(columns=["diff_dias"])

    values = [df.columns.tolist()]
    values.extend(df.values.tolist())

    print(df.dtypes)
  
    # Autenticar e criar serviço
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    
    try:
        # Limpar a aba existente (opcional)
        sheet.values().clear(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            body={}
        ).execute()

        # Escrever os dados na planilha
        request = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body={"values": values}
        )
        response = request.execute()

        print(f"Dados enviados com sucesso para {sheet_name} na planilha {spreadsheet_id}")
        return response
    except HttpError as err:
        print(err)
        return None

if __name__ == "__main__":
    # Configurações - altere conforme necessário
    EXCEL_FILE = "relatorio_atualizado.xlsx"  # Seu arquivo Excel
    SHEET_NAME = "teste"  # Nome da aba no Google Sheets
    SPREADSHEET_ID = "1DQAUJlgrTerE_zJ9e7e1boT32n18ZYdZaqKfuC0ZUFI"  # ID da planilha
    RANGE_NAME = f"{SHEET_NAME}!A1"  # Range onde os dados serão escritos (A1 = canto superior esquerdo)
    
    # Chamar a função para enviar os dados
    excel_to_google_sheets(EXCEL_FILE, SHEET_NAME, SPREADSHEET_ID, RANGE_NAME)