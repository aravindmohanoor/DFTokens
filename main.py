import json

import PySimpleGUIQt as sg
from dotenv import load_dotenv
from google.auth.transport import requests as google_requests
from google.oauth2 import service_account

load_dotenv()
font = ("Arial", 14)
first_column = [
    [
        sg.Text("Choose the service account JSON file"),
        sg.In(size=(25, 1), enable_events=True, key="-SINGLEFILE-"),
        sg.FileBrowse("Browse", size=(15, 1)),
    ],
    [sg.Text('Project ID:', size=(15,1))],
    [sg.Multiline(size=(100, 2), key='tb_project_id')],
    [sg.Text('Access Token:', size=(15, 1))],
    [sg.Multiline(size=(100, 10), key='tb_access_token')]
]

layout = [
    [
        sg.Column(first_column)
    ]
]

window = sg.Window("DFTokens", layout, font=font)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-SINGLEFILE-":
        json_file = values["-SINGLEFILE-"]
        with open(json_file, 'r') as f:
            contents = json.load(f)
            print(contents['project_id'])
            CREDENTIAL_SCOPES = ["https://www.googleapis.com/auth/dialogflow"]
            CREDENTIALS_KEY_PATH = f.name
            credentials = service_account.Credentials.from_service_account_file(
                CREDENTIALS_KEY_PATH, scopes=CREDENTIAL_SCOPES)
            credentials.refresh(google_requests.Request())
            bearer_token = credentials.token
            window['tb_project_id'].update(contents['project_id'])
            window['tb_access_token'].update(bearer_token)
window.close()
