# %%
import numpy as np
import pandas as pd
import datetime
import pygsheets
import requests
import os
import zipfile
import io
from google.oauth2 import service_account

# %%
def line_notify(msg):
    """
    Send message to targeted LINE account.

    Args:
        msg (str): Text message.
    """

    url = 'https://notify-api.line.me/api/notify'
    token = os.environ.get('line_token')
    headers = {'content-type': 'application/x-www-form-urlencoded',
               'Authorization': 'Bearer '+token}
    r = requests.post(url, headers=headers, data={'message': msg})
    print(f"LINE Notify | Status Code : {r.status_code}")

# %%
def get_covid_data():
    """
    Get COVID data from government API.

    Returns:
        dataframe of today's data
    """

    print('Start getting today COVID data')
    url = "https://covid19.th-stat.com/api/open/today"
    r = requests.get(url)
    df = pd.DataFrame(r.json(), index = [0])
    df = df.rename(columns = {'UpdateDate': 'UpdateDatetime'})
    df['UpdateDate'] = pd.to_datetime(df['UpdateDatetime']).dt.date
    df['UpdateDatetime'] = pd.to_datetime(df['UpdateDatetime'])
    df['GSheetUpdateDatetime'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    df_final = df[['UpdateDate', 'UpdateDatetime', 'GSheetUpdateDatetime', 'Confirmed', 'Recovered', 'Hospitalized', 'Deaths', 'NewConfirmed', 'NewRecovered', 'NewHospitalized', 'NewDeaths']].copy()
    print('Done getting today COVID data')
    return df_final

# %%
def paste_to_gsheet(df):
    """
    Paste daily COVID data to Google Sheet

    Args:
        df: dataframe of COVID data
    """

    print('Authorizing Google Sheet...')
    _SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
    service_account_info = {
        "type": "service_account",
        "project_id": os.environ.get('cred_project_id'),
        "private_key_id": os.environ.get('cred_private_key_id'),
        "private_key": os.environ.get('cred_private_key').replace('\\n', '\n'),
        "client_email": os.environ.get('cred_client_email'),
        "client_id": str(os.environ.get('cred_client_id')),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ.get('cred_client_x509_cert_url')
    }
    credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=_SCOPES)

    c = pygsheets.authorize(custom_credentials = credentials)
    sh = c.open('daily_th_covid_cases')
    wks = sh.worksheet('title','Data')

    df_gsheet = wks.get_as_df(start="A1", numerize=False)
    last_row = df_gsheet.index[-1]+3

    wks.set_dataframe(df,(last_row,1), copy_head = False)
    return_text = f"Done updating data in Google Sheet | {datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}"
    print(return_text)
    return return_text

# %%
line_notify(paste_to_gsheet(get_covid_data()))
