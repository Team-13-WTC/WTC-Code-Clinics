import smtplib
import ssl

def booked_event(username, event):
    """
    Retrieves username of volunteer and formulates message for booking an event
    Sends message and volunteer data to send_mail function
    Parameter:  username (local client), event (to be booked)
    Returns:    nothing
    """

    # creator of event's username
    volunteer = (event['attendees'][0]['email']).split('@')[0]
    
    # body of message to be sent
    message = f"""\
Subject: Code Clinic - booking
Good day {volunteer}.
The following Code Clinic event has been booked by {username}.
Title:               {event['summary']}
Date:              {event['start']['dateTime'][:10]}
Time:              {event['start']['dateTime'][11:16]}
Description:    {event['description']}
Regards
WTC"""

    send_mail(volunteer, message)

def cancelled_event(username, event):
    """
    Retrieves username of volunteer and formulates message for canceling an event
    Sends message and volunteer data to send_mail function
    Parameter:  username (local client), event (to be cancelled)
    Returns:    nothing
    """
    
    # creator of event's username
    volunteer = (event['attendees'][0]['email']).split('@')[0]
    
    # body of message to be sent
    message = f"""\
Subject: Code Clinic - cancelation
Good day {volunteer}.
The following Code Clinic event has been cancelled by {username}.
Title:               {event['summary']}
Date:              {event['start']['dateTime'][:10]}
Time:              {event['start']['dateTime'][11:16]}
Description:    {event['description']}
Regards
WTC"""

    send_mail(volunteer, message)


def send_mail(volunteer, message):
    """
    Using Google's smtp server and Code Clinic's email credentials, 
    sends the volunteer emails on changes to their events
    Parameter:  volunteer (creator's username), message (body to send)
    Returns:    nothing
    """

    # set variables to be used by smtplib
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "alessiodew@gmail.com"  
    password = "Alessio522%."
    receiver_email = f'{volunteer}@student.wethinkcode.co.za' 

    # use smtplib to login to email account and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)