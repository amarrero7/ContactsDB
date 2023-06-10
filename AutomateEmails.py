import os
import openpyxl
import win32com.client as win32

# Get the current working directory
cwd = os.getcwd()

# Load the Excel workbook
workbook = openpyxl.load_workbook(os.path.join(cwd, "contacts-for-verification.xlsx"))

# Select the sheet
sheet = workbook["contacts-for-verification"]

# Get the Outlook application object
outlook = win32.Dispatch('outlook.application')

# Iterate through the rows in the sheet
for i in range(1, 3):

    # Get the recipient email address
    recipient_email = sheet.cell(row=i, column=1).value

    # Create a new email
    mail = outlook.CreateItem(0)

    # Set the recipient and CC email addresses
    mail.To = recipient_email

    # Set the email subject
    mail.Subject = f"Updated Contact Information Request"

    body = ""
    with open("mailBody.txt", "r") as f:
        for line in f:
            body += line

    # Set the email text
    mail.Body = body

    # Open the email in Outlook
    mail.Display()
    
# close all opened objects
workbook.close()