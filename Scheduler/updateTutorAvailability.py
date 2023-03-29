from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError

from Scheduler import db
from sqlite3 import Error

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def DBFromEvents(id):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            os.remove('token.json')
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        oneWeekFromNow = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'

        sql = """
            SELECT avail_calendar FROM Tutor WHERE id = ?"""
        cur = db.cursor()
        cur.execute(sql, [id])

        calendarId = cur.fetchone()[0]
        
        events_result = service.events().list(calendarId=calendarId, timeMin=now,
                                              timeMax=oneWeekFromNow, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        sql = """
                DELETE FROM Tutor_Availability WHERE tutor_id = ?;"""
        db.execute(sql, [id])

        for event in events:
            start = event['start'].get('dateTime')
            end = event['end'].get('dateTime')
            start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
            end = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')
            weekdays = ['S', 'M', 'T', 'W', 'R', 'F']
            weekday = weekdays[start.isoweekday()]
            start = (start - datetime.timedelta(hours=12)).time().isoformat()
            end = (end - datetime.timedelta(hours=12)).time().isoformat()
            start = start[1:-3]
            end = end[1:-3]

            sql = """
                INSERT INTO Tutor_Availability(tutor_id, day, start, finish)
                VALUES(?, ?, ?, ?);"""
            db.execute(sql, [id, weekday, start, end])

            db.commit()

        return '', 200

    except HttpError as error:
        print(error)
        return error.reason, error.status_code
    except Error as e:
        print(e)
        return e.sqlite_errorname, 500
    except Exception as e:
        print(e)
        return e.args[0], 500

def eventsFromDB(id):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        sql = """
            SELECT avail_calendar FROM Tutor WHERE id = ?"""
        cur = db.cursor()
        cur.execute(sql, [id])

        calendarId = cur.fetchone()[0]

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        sql = """SELECT * FROM Tutor_Availability WHERE tutor_id = ?;"""
        cur = db.cursor()
        cur.execute(sql, [id])

        availablities = cur.fetchall()

        for availablity in availablities:
            # format 2023-02-25T09:00:00-07:00
            date = next_weekday(datetime.date.today() + datetime.timedelta(days=7), availablity[1]).isoformat()
            start = (datetime.datetime.strptime(availablity[2], '%H:%M') + datetime.timedelta(hours = 12)).time().isoformat()
            end = (datetime.datetime.strptime(availablity[3], '%H:%M') + datetime.timedelta(hours = 12)).time().isoformat()
            event = {
                'summary': 'Available',
                'description': 'Generated by Treehouse Tutoring Scheduler',
                'start': {
                    'dateTime': date + 'T' + start,
                    'timeZone': 'America/Los_Angeles'
                },
                'end': {
                    'dateTime': date + 'T' + end,
                    'timeZone': 'America/Los_Angeles'
                }
            }
            # print(date, start, end)
            event = service.events().insert(calendarId=calendarId, body=event).execute()
            print('event created:', event.get('htmlLink'))

        return '', 201

    except HttpError as error:
        print(error)
        return error.reason, error.status_code
    except Error as e:
        print(e)
        return e.sqlite_errorname, 500
    except Exception as e:
        print(e)
        return e.args[0], 500

def next_weekday(d, weekday):
    weekdays = {
        'M': 0,
        'T': 1,
        'W': 2,
        'R': 3,
        'F': 4
    }
    days_ahead = weekdays[weekday] - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)