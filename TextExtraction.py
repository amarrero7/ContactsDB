import requests
from bs4 import BeautifulSoup
import os

def extract_text_from_webpage(url):
    response = requests.get(url)
    # with open("inter_ponce_web_html.txt", 'w', encoding='utf-8') as file:
    #     file.write(response.text)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_text = soup.get_text()
        return main_text
    else:
        return None

# webpage_url = f"https://cit.ponce.inter.edu/ipform/Directorio-Facultad/f?n=e6630df9-23cf-4e78-a13a-4a2b7b4c2154"
# webpage_text = extract_text_from_webpage(webpage_url)

# if webpage_text is not None:
#     pass
# else:
#     print('error')

# with open("inter_ponce_web_html.txt", 'r', encoding='utf-8') as f1:
#     with open('inter_ponce_faculty_info_links.txt', 'a', encoding='utf-8') as f2:
#         for line in f1:
#             if line.find('href=') != -1:
#                 f2.write(line.strip('\n') + '\n')

profile_links = []
with open("inter_ponce_faculty_info_links.txt", 'r', encoding="utf-8") as file:
    for line in file:
        end = line.find('"')
        profile_links.append(line[0:end].strip('\n'))

for link in profile_links:
    profile_text = extract_text_from_webpage("https://cit.ponce.inter.edu/ipform/Directorio-Facultad/" + link.strip('\n'))
    if profile_text is not None:
        with open('raw_profile_data.txt', 'w', encoding='utf-8') as file:
            file.write(profile_text)
        with open('raw_profile_data.txt', 'r', encoding='utf-8') as raw_input:
            with open('filtered_profiles.txt', 'a', encoding='utf-8') as output:
                for line in raw_input:
                    if line != "\n" and not line.startswith(" "):
                        output.write(line.strip('\n') + '\n')
                output.write("------------------------------------------------------------------" + '\n')
    os.remove('raw_profile_data.txt')


# with open("emails_rcm_anatomia_neurobiologia.txt", "r", encoding="utf-8") as file1:
#     with open("emails_rcm_anatomia_neurobiologia.txt", "a", encoding="utf-8") as file2:
#         c = 0
#         for line in file1:
#             email = ""
#             end = line.index('.edu')
#             email = line[0:end+4]
#             print(email)
#             c += 1
#             # file2.write(email + '\n')
#         print(c)




