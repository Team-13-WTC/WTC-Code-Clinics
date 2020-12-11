from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich import box
import json

def get_slots(data):
    """
    This function selects the data to be queried from the json file
    """

    event_id = data['id']
    description = data['description'] #specialty
    creator = list(data['creator'].values())[0] #volunteer's email
    start = list(data['start'].values())[0].replace("T", " ")[0:16] #print with spaces
    end = list(data['end'].values())[0][11:16]
    return f"[b][white]ID: {event_id}\n[turquoise2]{creator}\n[green]{start} [b][white]| [green]{end}\n[deep_sky_blue3]{description}"

def get_volunteerd(data):
    """
    This will pick the type of data     should be displayed when requesting slots volunteerd for.
    :Parameter data : the data that will be traversed.
    """

    #add attendees if attendee greater than 1
    event_id = data['etag']
    description = data['description'] #specialty
    creator = list(data['attendees'][0].values())[0] #if attendee present creator > attendee 
    start = list(data['start'].values())[0].replace("T", " ")[0:16] #print with spaces
    end = list(data['end'].values())[0][11:16]
    return f"[b][white]ID: {event_id}\n[turquoise2]{creator}\n[green]{start}  [b][white]| [green]{end}\n[deep_sky_blue3]{description}"

def get_booked_slots(data):
    """
    Get booked slots type data
    """

    #add attendees if attendee greater than 1
    event_id = data['id']
    description = data['description'] #specialty
    creator = list(data['attendees'][0].values())[0] #if attendee present creator > attendee 
    start = (list(data['start'].values())[0]).replace("T", " ")[0:16] #print with spaces
    end = list(data['end'].values())[0][11:16]
    
    return f"[b][white]ID: {event_id}\n[turquoise2]{creator}\n[green]{start}  [b][white]| [green]{end}\n[deep_sky_blue3]{description}"


def get_personal(data):
    """
    This will pick the type of data should be displayed when requesting slots volunteerd for.
    :Parameter data : the data that will be traversed.
    """

    creator = list(data['creator'].values())[0] #if attendee present creator > attendee 
    start = list(data['start'].values())[0].replace("T", " ")[0:16] #print with spaces
    end = list(data['end'].values())[0][11:16]
    return f"[b][turquoise2]{creator}\n[green]{start}  [b][white]| [green]{end}"


"""
Could do this in a better way.
Need to ask the team.
"""

def display_slots(data, data_type):
    """
    Displays the  slot data
    :data : will be the calendar data
    :type_data : will be the header for the border eg. "BOOKED", "SLOTS"
    """
    console = Console()
    user_render = [Panel(get_slots(user), expand=False, title=data_type,box=box.HEAVY_HEAD, border_style="pale_turquoise1") for user in data]
    console.print(Columns(user_render))

def display_volunteerd(data, data_type):
    """
    Displays the  volunteer data
    :data : will be the calendar data
    :type_data : will be the header for the border eg. "BOOKED", "SLOTS"
    """
    console = Console()
    user_render = [Panel(get_volunteerd(user), expand=False, title=data_type,box=box.HEAVY_HEAD, border_style="pale_turquoise1") for user in data]
    console.print(Columns(user_render))

def display_booked_slots(data, data_type):
    """
    Displays the  booked slot data
    :data : will be the calendar data
    :type_data : will be the header for the border eg. "BOOKED", "SLOTS"
    """

    console = Console()
    user_render = [Panel(get_booked_slots(user), expand=False, title=data_type,box=box.HEAVY_HEAD, border_style="pale_turquoise1") for user in data]
    console.print(Columns(user_render))

def display_personal(data, data_type):
    """
    Displays the  personal calendar data
    :data : will be the calendar data
    :type_data : will be the header for the border eg. "BOOKED", "SLOTS"
    """

    console = Console()
    user_render = [Panel(get_personal(user), expand=False, title=data_type,box=box.HEAVY_HEAD, border_style="pale_turquoise1") for user in data]
    console.print(Columns(user_render))
