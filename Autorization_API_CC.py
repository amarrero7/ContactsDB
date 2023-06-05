import pandas
import json
import requests
import time
import webbrowser

url = 'https://authz.constantcontact.com/oauth2/default/v1/device/authorize'
data = {
    'client_id': "32fe8fe3-8097-4701-bebd-990b8a79a7e6",
    'scope': "contact_data account_update offline_access account_read",
}

autorization_request = requests.post(url, data=data)
access_token = None

# JSON reponse contents
# device_code = autorization_request.json()['device_code']
# user_code = autorization_request.json()['user_code']
# verification_uri = autorization_request.json()['verification_uri']
# expires_in = autorization_request.json()['expires_in']
# interval = autorization_request.json()['interval']
verification_uri_complete = autorization_request.json()['verification_uri_complete']
device_code = autorization_request.json()['device_code']
webbrowser.open(verification_uri_complete)

verified = input("Have you autorized the app? (y/n): ")

if verified == "y" or "Y":
    access_token_url = "https://authz.constantcontact.com/oauth2/default/v1/token"

    data = {
        'client_id': "32fe8fe3-8097-4701-bebd-990b8a79a7e6",
        'device_code': device_code,
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
    }

    headers = {
        'content_type': 'application/x-www-form-urlencoded',
    }

    access_token_request = requests.post(access_token_url, data=data, headers=headers)

    access_token = access_token_request.json()['access_token']

if access_token != None:
    print("Access token granted")

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
}

url = 'https://api.cc.email/v3/contact_lists'

response = requests.get(url, headers=headers, )

if response.status_code == 200:
    print("Success")
else:
    print("Error: ", response.status_code)

target_list_id = None
for list in response.json()['lists']:
    if list['name'] == "TEST CONTACTS UPDATE":
        target_list_id = list['list_id']

# Adding contact
contact_data = {
    "email_address": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "list_memberships": ["97de3134-03db-11ee-9a40-fa163e5fbd10"]
}
endpoint = f"https://api.cc.email/v3/contacts/sign_up_form"

response = requests.post(endpoint, headers=headers, json=contact_data)

if response.status_code == 201:
    print("Success")
else:
    print("Error: ", response.status_code)

