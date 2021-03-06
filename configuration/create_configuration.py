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
import hashlib
import json
from typing import Dict, Any
from interface import validations

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 
'https://www.googleapis.com/auth/calendar']

configparser = ConfigParser()

home_dir = str(Path.home())
conf_dir = ".clinic_config/" #the configuration folder name
store_dir = ""
conf_name = "clinic.conf"
config_path = "./clinic.conf"
full_config = home_dir + "/" + conf_dir + conf_name
config_home_dir = home_dir + "/" + conf_dir
service = ''


def user_login():
    """
    User Login- creates and/or stores user's account information and permits
    access to Google Calendar API 
    Return: the api servive object
    """

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(config_home_dir + 'token.pickle'):
        with open(config_home_dir + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            print("Configuration created successfully.")
        # Save the credentials for the next run
        with open(config_home_dir + '/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def temp_config_dir(config_dir):
    """
    Creates a temp configuration directory if one does not exist to be passed to
    config setup
    Parameter: config_dir - takes this in to check if it exists
    Return: conf_dir
    """
 
    print(home_dir + "/" + conf_dir)
    if not path.exists(home_dir + config_dir):
        os.system("mkdir " + config_home_dir)
    return config_dir


def create_config_dir():
    """
    This will create the hidden directory on the users home directory. The 
    token.pickle is also moved to the hidden directory
    Parameter:home_dir is the users home dir, you run `echo $HOME` to see this
    Parameter:config_dir is the hidden directory name
    """

    global home_dir, config_dir

    if not path.exists(home_dir + conf_dir):
        subprocess.run(['mkdir', home_dir + conf_dir])
    if path.exists('token.pickle'):
        subprocess.run(['mv', 'token.pickle', home_dir + conf_dir])


def create_config(service, conf_name):
    """
    Writes to config file storing relevant user information - username, campus,
    secondary calendar once only
    Parameter: service
    Parameter: conf_name
    """
    global store_dir

    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])
    
    exist = False

    user_name  = input("User name : ")
    campus  = input("Campus : CPT/JHB : ")

    calendars_days = input("Days limit: ")
    #The user must enter a valid day so we don't run into execution errors
    while not validations.days_are_valid(calendars_days):
        calendars_days = input("Days limit: ")

    #The user must enter a valid calendar so we don't run into execution errors
    while not exist:
        calendar = input("Calendar: ")
        for cal in calendars:
            if calendar.lower() == cal['summary'].lower():
                calendar_id = cal['id']
                exist = True

    configparser['user_info'] = {}
    configparser['user_info']['username'] = user_name.lower()
    configparser['user_info']['campus'] = campus.lower()
    configparser['user_info']['calendar'] = calendar_id
    configparser['user_info']['days_to_get'] = calendars_days

    with open(full_config, 'w') as config:
        configparser.write(config)


def retrieve_variable(variable):
    """
    Extracts the appropriate parameter stored in config file, either cal_days,
    user_name or no_cal_days
    Parameter: variable -user_name, campus, calendars_days or calendar
    Return: 
    """

    config_object = ConfigParser()
    config_object.read(full_config)
    userinfo = config_object["user_info"]    
    return userinfo[variable]


def update_config_date(days):
    """
    Updates calendar_days in config file and writes over old days
    Parameter: days
    """
    global config_path

    config_object = ConfigParser()
    config_object.read(config_path)

    config_object["user_info"]['days'] = days

    with open(config_path, 'w') as update:
        config_object.write(update)


def setup_config():
    """
    Creates the hidden configuration directory in user' home directory and
    initiates Google API connection
    """

    if not path.exists(config_home_dir):
        temp_config_dir(config_home_dir)
        service = user_login()
        create_config(service, conf_name)


def check_calender_state(system_calendar_file, service):
    """
    This function will check if the calender data has been updated. It will md5
    hash the requested json data and the json the file system. After it gets the
    md5 hashes it will compare them. If the hashes are identical then the
    calender hasn't changed if they're different the calender has changed.
    Parameter: system_calendar - json file name where calendar info is stored
    Parameter: API service object
    Return: True if there were no changes to calendar over that specified time

    """

    requested_calendar = service.events().list(calendarId=retrieve_variable('calendar')).execute()

    with open(system_calendar_file) as read_system_file:
        system_file_data = json.load(read_system_file)

    hashed_sys_f = dictionary_hash(system_file_data)
    hashed_req_file = dictionary_hash(requested_calendar)

    if hashed_req_file == hashed_sys_f:
        return True
    return False


def dictionary_hash(json_data: Dict[str, Any]) -> str:
    """
    The json data saves as a dictinary so we'll md5 the dictionary.
    The -> tells the function to return a string
    Parameter: dhash is an object, it holds the hash. initially it's empty but
    we give it the encoded json data.
    Return: Hashlib returns the md5 hash in hexadecimal and we use hexdigest
    to make it ascii
    """
    dhash = hashlib.md5()

    encoded = json.dumps(json_data, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()
