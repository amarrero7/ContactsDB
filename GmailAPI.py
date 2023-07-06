from __future__ import print_function
import datetime
import pandas as pd
import json
import requests
import time
import webbrowser
import os
import openpyxl
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

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
            r'c:\Users\aleja\Desktop\Python CM\ContactsDB\creds.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(r'c:\Users\aleja\Desktop\Python CM\token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('gmail', 'v1', credentials=creds)
    print('Connection Succesful')
except HttpError as err:
        print(err)

def get_labels():
    response = service.users().labels().list(userId='me').execute()
    labels = response.get('labels', [])
    for label in labels:
        print(label)

def retrieve_messages():
    page_token = "11339957112772947555"
    messages = []

    # Convert the start and end dates to epoch time in seconds
    start_date = '2019-01-01'
    end_date = '2020-01-01'
    start_time = int(datetime.datetime.strptime(start_date, '%Y-%m-%d').timestamp())
    end_time = int(datetime.datetime.strptime(end_date, '%Y-%m-%d').timestamp())

    # Set the query with the after and before parameters
    query = f'after:{start_time} before:{end_time}'

    while True:
        response = service.users().messages().list(userId='me', pageToken=page_token, q=query).execute()
        messages.extend(response.get('messages', []))
        page_token = response.get('nextPageToken')
        if not page_token or len(messages) == 1100:
            with open("next_page_token.txt", 'w') as f:
                f.write(page_token)
            break

    return messages

def get_subject_and_date(message_id):
    message_data = service.users().messages().get(userId='me', id=message_id, format='metadata').execute()
    subject = ''
    date = ''
    for header in message_data['payload']['headers']:
        if header['name'] == 'Subject':
            subject = header['value']
        if header['name'] == 'Date':
            date = header['value']

    # Convert date string to a datetime object
    datetime_obj = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')
    # Format the datetime object as desired
    formatted_date = datetime_obj.strftime('%Y-%m-%d')

    return subject, formatted_date

def is_message_read(message_id):
    message_data = service.users().messages().get(userId='me', id=message_id, format='metadata').execute()
    label_ids = message_data['labelIds']
    
    return 'UNREAD' not in label_ids

def add_label_to_message(message_id, label_id):
    modify_request = {
        'addLabelIds': [label_id]
    }
    service.users().messages().modify(userId='me', id=message_id, body=modify_request).execute()

def check_new_messages():
    history_response = service.users().history().list(userId='me', startHistoryId="39427081").execute()
    changes = history_response.get('history', [])
    
    if changes:
        for change in changes:
            if 'messagesAdded' in change:
                message_ids = [msg['message']['id'] for msg in change['messagesAdded']]
                print('New messages have been received.')
                print('Message IDs:', message_ids)
            else:
                continue
    else:
        print('No new messages.')

def get_start_history_id():
    profile = service.users().getProfile(userId='me').execute()
    return profile['historyId']


def main():
    print("Retrieving messages...")
    test = retrieve_messages()
    print("Completed")
    print('----------------------------------\n')
    emails = []
    emails_set = set()
    print("Retrieving emails...")
    for message in test:
        message_id = message.get('id')
        message_data = service.users().messages().get(userId='me', id=message_id, format='metadata').execute()
        for header in message_data['payload']['headers']:
            if header['name'] == 'To':
                emails.extend(header['value'].split(','))
    print("Completed")
    print('----------------------------------\n')
    for email in emails:
        emails_set.add(email.strip())
    with open("emails_list_2019_2020.txt", 'w') as f:
        for e in emails_set:
            if e.find('@bioanalytica') == -1:
                f.write(e + '\n')
    
    return 0

if __name__ == '__main__':
    main()
    pass




