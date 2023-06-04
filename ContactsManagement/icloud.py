import pyicloud as pci
import sys 

#Login
api = pci.PyiCloudService('alejandromarrero89@gmail.com', 'Colegio8990-', cookie_directory=None)
api.authenticate(force_refresh=True)

if api.requires_2fa:
    print("Two-factor authentication required.")
    code = input("Enter the code you received of one of your approved devices: ")
    result = api.validate_2fa_code(code)
    print("Code validation result: %s" % result)

    if not result:
        print("Failed to verify security code")
        sys.exit(1)

    if not api.is_trusted_session:
        print("Session is not trusted. Requesting trust...")
        result = api.trust_session()
        print("Session trust result %s" % result)

        if not result:
            print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
elif api.requires_2sa:
    import click
    print("Two-step authentication required. Your trusted devices are:")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print(
            "  %s: %s" % (i, device.get('deviceName',
            "SMS to %s" % device.get('phoneNumber')))
        )

    device = click.prompt('Which device would you like to use?', default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print("Failed to send verification code")
        sys.exit(1)

    code = click.prompt('Please enter validation code')
    if not api.validate_verification_code(device, code):
        print("Failed to verify verification code")
        sys.exit(1)

# Retrives Contacts and Their Phone Number
def contacts():
    contacts_cont = []
    for c in api.contacts.all():
        if (c.get('firstName') != None):
            try:
                reference = {"name": c.get('firstName'), "phone": c.get('phones')[0]['field'], "email": c.get('emailAddresses')[0]['field']}
            except:
                reference = {"name": c.get('firstName'), "phone": c.get('phones')[0]['field'], "email": c.get('emailAddresses')}
            contacts_cont.append(reference)
    return contacts_cont
