import smtplib, ssl

def booked_event(username, event):
    
    volunteer = (event['attendees'][0]['email']).split('@')[0]
    
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
    
    volunteer = (event['attendees'][0]['email']).split('@')[0]
    
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
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "alessiodew@gmail.com"  
    password = "Alessio522%."
    receiver_email = f'{volunteer}@student.wethinkcode.co.za' 

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)