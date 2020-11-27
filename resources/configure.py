from __future__ import print_function
from os import path
import subprocess
from configparser import ConfigParser
import datetime
import pickle
from datetime import timedelta
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from os import system
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar']

configparser = ConfigParser()

def user_login():
    """Logs the user in and checks for other stuff
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def config_dir():
    if not path.exists('.code_clinic'):
        subprocess.run(['mkdir', '.code_clinic'])
    if path.exists('token.pickle'):
        subprocess.run(['mv', 'token.pickle', '.code'])

    # if not path.exists(home_d)


def create_config():
    if not path.exists('.code_clinic'):
        subprocess.run(['mkdir', '.code_clinic'])
    if path.exists('token.pickle'):
        subprocess.run(['mv', 'token.pickle', '.code'])

    #might add a little more fields if we need them
    user_name  = input("User name : ")
    campus  = input("Campus CPT/JHB : ")
    calendar  = input("Calendar : ")

    configparser['user_info'] = {}

    configparser['user_info']['username'] = user_name
    configparser['user_info']['campus'] = campus
    configparser['user_info']['calendar'] = calendar

    with open('.code_clinic/wtc_clinic.config', 'w') as config:
        configparser.write(config)

service = user_login()

# create_event("Code", "cpt", "Love does exist Hiranya :)", '2020-11-15', '15:00', 'sshandu', service)

create_config()

