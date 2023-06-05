import pandas as pd
import openpyxl

df = pd.read_excel(r"c:\Users\aleja\Desktop\contacts-for-verification.xlsx")

emails = df["Email address"].tolist()

with open(r"c:\Users\aleja\Desktop\emails_only.txt", "w") as f:
    for e in emails:
        f.write(e + "\n")
