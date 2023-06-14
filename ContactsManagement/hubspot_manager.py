import hubspot as hb
import icloud
import json
from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException

# API
api_client = hb.HubSpot(access_token='None')

def create_contact(args):
    try:
        simple_public_object_input = SimplePublicObjectInput(
            properties= {"phone": args['phone'] ,"firstname": args['name']}
        )
        api_response = api_client.crm.contacts.basic_api.create(
            simple_public_object_input=simple_public_object_input
        )
    except ApiException as e:
        print("Exception when creating contact: %s\n" % e)

contacts_data = icloud.contacts()
# test_contact = (contacts_data[0]['name'], contacts_data[0]['phone'])
for contact in contacts_data:
    create_contact(contact)

