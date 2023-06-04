import pandas as pd
import json
import constantcontact
import requests
import time
import contacts_db 

data = contacts_db.data

print(len(data))

columns = ["Email", "First Name", "Last Name", "Organization", "Status", "Added By", "Date Added"]

df = pd.DataFrame(data, columns=columns)
excel_file = r"c:\Users\aleja\Desktop\Contacts_DB_Test.xlsx"
df.to_excel(excel_file, index=False)


    
