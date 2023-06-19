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
    with open('contactos_vacios2.txt', 'r', encoding='utf-8') as file1:
        for line in file1:
            contactos.append(line.strip('\n'))
    
    while True:
        pbot.leftClick(234, 220)
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

enter_contact()