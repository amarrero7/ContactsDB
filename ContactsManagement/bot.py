import pyautogui as pbot
import time

def show_mouse_position():
    pbot.displayMousePosition()

def get_duplicates():
    contactos = []
    resultado = []
    with open('allContacts.txt', 'r', encoding='utf-8') as file1:
        for line in file1:
            contactos.append(line.strip('\n'))
    for c in contactos:
        if contactos.count(c) > 1 and not c in resultado:
            resultado.append(c)
    return resultado

def enter_contact():
    # Get the contact list
    contactos = []
    contact_position = 0
    with open(r'C:\Users\aleja\Desktop\Python CM\ContactsDB\contactos_vacios2.txt', 'r', encoding='utf-8') as file1:
        for line in file1:
            contactos.append(line.strip('\n'))
    
    while True:
        pbot.leftClick(750, 150)
        pbot.hotkey('ctrl', 'a')
        pbot.press("backspace")
        pbot.leftClick(234,220)
        pbot.write(contactos[contact_position])
        time.sleep(2)
        pbot.leftClick(409,219)
        time.sleep(2)
        pbot.leftClick(411, 954)
        finish = input("Y/N")
        if finish == 'y' or finish == 'Y':
            print("Last contact accessed: " + str(contact_position + 1))
            break
        else:
            contact_position += 1
            continue

contact_position = 0
contacts = []
with open('emails_list_2019_2020.txt', 'r') as f:
    for line in f:
        try:
            line = line.strip()
            ind1 = line.index('<')
            ind2 = line.index('>')
            result = line[ind1 + 1:ind2]
            contacts.append(result)
        except:
            continue
while True:
    pbot.leftClick(750, 150)
    time.sleep(0.3)
    pbot.hotkey('ctrl', 'a')
    pbot.press("backspace")
    pbot.write(contacts[contact_position])
    pbot.press('enter')
    finish = input("Y/N")
    if finish == 'y' or finish == 'Y':
        print("Last contact accessed: " + str(contact_position + 1))
        break
    else:
        contact_position += 1
        continue

    