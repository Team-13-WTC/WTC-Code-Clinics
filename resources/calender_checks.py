import hashlib
import json
from typing import Dict, Any


def check_calender_state(system_calendar_file, service):
    """
    This function will check if the calender data has been updated,
    :It will md5 hash the requested json data and the json the file system
    :After it gets the md5 hashes it will compare them. if the hashes are identical then the calender hasn't changed if they're different the calender has changed somehow
    :Note : I think we could also use the Etag to check if the data has changed. 
    """

    requested_calendar = service.events().list(calendarId='primary').execute()

    with open(system_calendar_file) as read_system_file:
        system_file_data = json.load(read_system_file)

    hashed_sys_f = dict_hash(system_file_data)
    hashed_req_file = dict_hash(requested_calendar)

    if hashed_req_file == hashed_sys_f:
        return True
    return False

def dictionary_hash(json_data: Dict[str, Any]) -> str:
    """
    The json data saves as a dictinary so we'll md5 the dictionary.
    :The -> tells the function to return a string
    :dhash is an object, it holds the hash. initially it's empty but we give it the encoded json data.
    :Hashlib returns the md5 hash in hexadecimal and we use hexdigest to make it ascii
    """
    dhash = hashlib.md5()

    encoded = json.dumps(json_data, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()