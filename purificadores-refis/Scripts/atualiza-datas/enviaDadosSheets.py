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

def excel_to_google_sheets():
    excel_file = "relatorio_atualizado.xlsx"
    sheet_name = "Última Compra"
    spreadsheet_id = "1DQAUJlgrTerE_zJ9e7e1boT32n18ZYdZaqKfuC0ZUFI"
    range_name = f"{sheet_name}!A1"
    df = pd.read_excel(excel_file)

    for col in df.select_dtypes(include=["datetime", "datetimetz"]):
        if col != "dtmovimento":
            df[col] = df[col].astype(str)

    for col in df.columns:
        df[col] = df[col].fillna("")

    for col in df.columns:
        if col != "valtotliquido" and "dtmovimento"and "qtdproduto"and "idsubproduto"and "idclifor":
            df[col] = df[col].astype(str)
        
    if('diff_dias' in df.columns):
        df = df.drop(columns=["diff_dias"])
    
    values = [df.columns.tolist()]
    values.extend(df.values.tolist())
  
    # Autenticar e criar serviço
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    
    try:
        sheet.values().clear(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            body={}
        ).execute()

        request = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body={"values": values}
        )
        response = request.execute()
        return response
    
    except HttpError as err:
        print(err)
        return None
