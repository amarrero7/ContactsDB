import openpyxl
import webbrowser
import pyautogui as bot

# Load the Excel workbook
workbook = openpyxl.load_workbook(r"c:\Users\aleja\Desktop\CC_GROWTH_DB.xlsx")

# Select the sheet
sheet = workbook["INTER PONCE QUIMICA"]

# Parse through contacts
contactos = []

# with open(r"c:\Users\aleja\Desktop\RAW FACULTY DATA\molecular_science_faculty_info.txt", 'r', encoding='utf-8') as file1:
#     getting_name = True
#     name, email, position = "", "", ""
#     for line in file1:
#         if getting_name:
#             name = line.strip('\n')
#             getting_name = False
#         if line.startswith("position"):
#             start = line.find(":")
#             position = line[start+2::].strip('\n')
#         if line.startswith("Email"):
#             start = line.find(":")
#             email = line[start+2::].strip('\n')
#         if line.startswith("\n") or line == '\n':
#             contactos.append([name, email, position])
#             name, email, phone = "", "", ""
#             getting_name = True

with open(r"c:\Users\aleja\Desktop\RAW FACULTY DATA\inter ponce quimica.txt", 'r', encoding='utf-8') as file1:
    info = ""
    contact = []
    for line in file1:
        info += line
        if line == '\n':
            data = info.split('\n')
            contact.append(data[0].strip('\n'))
            contact.append(data[3].strip('\n'))
            contact.append("787-284-1912 ext." + data[4].strip('\n'))
            contact.append(data[1].strip('\n'))
            contact.append(data[2].strip('\n'))
            contactos.append(contact)
            contact = []
            info = ""
contact_pos = 0
for i in sheet.iter_rows(min_row=2, max_row=len(contactos) + 1):
    i[0].value = contactos[contact_pos][0]
    i[1].value = contactos[contact_pos][1]
    i[2].value = contactos[contact_pos][2]
    i[3].value = contactos[contact_pos][3]
    i[4].value = contactos[contact_pos][4]
    i[5].value = "INTER PONCE"
    contact_pos += 1

workbook.save(r"c:\Users\aleja\Desktop\CC_GROWTH_DB.xlsx")





