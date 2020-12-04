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
from pathlib import Path

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar']

configparser = ConfigParser()

home_dir = str(Path.home()) + "/" # $HOME dir of current user
conf_dir = ".clinic_config" #the configuration folder name
store_dir = ""
conf_name = "clinic.conf"
config_path = ".clinic_config/clinic.conf"

def user_login():
    """
    :User Login
    :Returns the api servive object
    """

    global home_dir, config_dir

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

def temp_config_dir():
    """
     Creates the temp configuration directory.
     We'll use this one for now.
     :conf_dir is the name of the config directory
     :home_dir will be where the conf_dir will be stored
    
    """
    config_dir = ".clinic_config"


    #for the testing 
    if not path.exists(config_dir):
        subprocess.run(['mkdir', conf_dir])
    if path.exists('token.pickle'):
        subprocess.run(['mv', 'token.pickle', config_dir])

    return config_dir


def create_config_dir():
    """
    This will create the hidden directory on the users home directory.
    :home_dir is the users home dir, you run `echo $HOME` to see this
    :config_dir is the hidden directory name
    :the token.pickle is also moved to the hidden directory
    """
    global home_dir, config_dir

    if not path.exists(home_dir + conf_dir):
        subprocess.run(['mkdir', home_dir + conf_dir])
    if path.exists('token.pickle'):
        subprocess.run(['mv', 'token.pickle', home_dir + conf_dir])

def create_config(service, conf_name):
    """
    Creates the configuration:
    Stores : username, campus, secondary calendar
    :The user must enter a valid calendar so we don't run into execution errors.
    """
    global store_dir

    # store_dir = temp_config_dir()

    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])
    
    exist = False
    #Don't judge this code
    user_name  = input("User name : ")
    campus  = input("Campus : CPT/JHB : ")
    calendars_days = input("Days limit: ")
    while not exist:
        calendar = input("Calendar: ")
        for cal in calendars:
            if calendar.lower() == cal['summary'].lower():
                calendar_id = cal['id']
                exist = True

    configparser['user_info'] = {}
    configparser['user_info']['days'] = calendars_days
    configparser['user_info']['username'] = user_name.lower()
    configparser['user_info']['campus'] = campus.lower()
    configparser['user_info']['calendar'] = calendar_id

    with open(store_dir + "/" +  conf_name, 'w') as config:
        configparser.write(config)

def update_config_date(days):
    global config_path

    config_object = ConfigParser()
    config_object.read(config_path)

    config_object["user_info"]['days'] = days

    with open(config_path, 'w') as update:
        config_object.write(update)
        
if not path.exists(conf_dir):
    store_dir = temp_config_dir()
    service = user_login()
    create_config(service, conf_name)