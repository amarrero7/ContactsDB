from __future__ import print_function
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

SCOPES = ['https://www.googleapis.com/auth/contacts']

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
    service = build('people', 'v1', credentials=creds)
except HttpError as err:
        print(err)

contacts_df = pd.read_excel(r"c:\Users\aleja\Desktop\contacts-for-verification.xlsx")
contacts_db = []
google_contacts_resource_names = []
found_contacts = []

for index, row in contacts_df.iterrows():
    if (index > 136):
        break
    contacts_db.append(row["Email address"])

def getGroup(group_name_str):
    # Call to get a list of groups or labels
    results = service.contactGroups().list().execute()
    for contact_group in results.get('contactGroups', []):
        label_name = contact_group.get('name', '')
        if label_name == group_name_str:
            label_resource_name = contact_group.get('resourceName', '')
            print(label_resource_name)
            break
# "Not Available (2023) label resourceName "
# contactGroups/6db106ad083ab4e5

def add_to_Label(label_resource_name, contact_resource_names):
    request_body = {
        'resourceNamesToAdd': contact_resource_names
    }

    label_resource_name = label_resource_name.split('/')[1]  # Extract the label_id from the resourceName

    service.contactGroups().members().modify(
        resourceName=f'contactGroups/{label_resource_name}',
        body=request_body
    ).execute()

# Call the People API
print("API Process..... \n")
with open("contacts_google_api.txt", 'w') as output:
    page_token = None
    while True:
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=2000,
            pageToken=page_token,
            personFields='names,emailAddresses'
        ).execute()

        connections = results.get('connections', [])

        for person in connections:
            email = person.get('emailAddresses', [])
            resourceName = person.get('resourceName')
            if email:
                address = email[0].get("value")
                if address in contacts_db:
                    # output.write(address + " --> ")
                    # output.write(resourceName)
                    # output.write('\n')
                    google_contacts_resource_names.append(str(resourceName))
                    found_contacts.append(address)
                else:
                    continue

        # Check if there are more pages
        if 'nextPageToken' in results:
            page_token = results['nextPageToken']
        else:
            break

add_to_Label("contactGroups/6db106ad083ab4e5", google_contacts_resource_names)

print("Process completed. \n")

print("Contacts that were not found in Google Contacts: \n")

not_found_contacts = []
counter = 0
for c in contacts_db:
    if not c in found_contacts:
        not_found_contacts.append(c)
        counter += 1

print( f"Total contacts not found:  {counter}" )

# Putting in a excel spreadsheet contacts that were not found

data = []
# format ("Email address", "First name", "Last name", "Company", "Job title") 
for index, row in contacts_df.iterrows():
    email_address = row["Email address"] 
    if email_address in not_found_contacts:
        data.append( (email_address, row["First name"], row["Last name"], row["Company"], row["Job title"]) )
        
columns = ["Email address", "First name", "Last name", "Company", "Job title"] 

not_found_contacts_df = pd.DataFrame(data, columns=columns)   
excel_file = r"c:\Users\aleja\Desktop\ContactsNotFound-GoogleContacts.xlsx"  
not_found_contacts_df.to_excel(excel_file, index=False)








