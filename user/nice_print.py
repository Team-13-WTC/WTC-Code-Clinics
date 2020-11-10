from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
import json

def get_calender_data(data_file):
    """
    The data_file must be a dictionary
    This function loads data from a json file
    """
    with open(data_file, 'r') as json_data:
        data = json.load(json_data)
    return (data)

def get_content(data):
    """
    This function can be modified to get which ever data is desired
    This function selects the data to be queried from the json file
    """
    etag = data['etag']
    description = data['description']
    creator = list(data['creator'].values())[0]
    start = list(data['start'].values())[0]
    end = list(data['end'].values())[0]
    return f"{etag}\n[purple]{creator}\n[green]{start} [red]{end}\n[b][yellow]{description}"

def display_slots(data):
    """
    This function will take the dictionary data as the argument and pass it to get_content, and loop through the events and print them with style :)
    """
    data = get_calender_data(data)
    console = Console()
    # console.print(data, overflow='ignore', crop=False) If you want to print out the json data too
    user_render = [Panel(get_content(user), expand=True) for user in data['items']]
    console.print(Columns(user_render))





