import json
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from google.oauth2.credentials import Credentials


def get_creds(SCOPES):
    '''
    Function to get the google sheet credentials from the credentials.json downloaded from Google Console
    :param SCOPES: Defines the access limits of Google sheets.
    :return: creds: Credentials to access our account Google Sheets
    '''
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', "w") as f:
            f.write(creds.to_json())
    return creds


def get_sheet_data(scopes, spreadsheet_id, sample_range):
    """
    Function that fetches google sheet data using given inputs
    :param scopes: Defines the access limits of Google sheets.
    :param spreadsheet_id: ID of the spreadsheet you want to access through api
    :param sample_range: Range of cells you want to access in a sheet. It can be entire spreadsheet too.
    :return:
    """
    creds = get_creds(scopes)
    try:
        # Call the Sheets API
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId = spreadsheet_id,
            range=sample_range).execute()
        values = result.get('values', [])
        if not values:
            print('No Data Found')
            return 'No Data Found'
        else:
            return values
    except HttpError as err:
        print(err)
        return err


if __name__ == '__main__':
    # While modifying the SCOPES, delete the token.json file
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # The ID and range of sample spreadsheet
    SPREADSHEET_ID = '<your sheet id>'
    SAMPLE_RANGE = 'Sheet1'
    data = get_sheet_data(SCOPES, SPREADSHEET_ID, SAMPLE_RANGE)
    df = pd.DataFrame(data[1:], columns=list(data[0]))
    df = df.set_index('Index')
    print(df)






