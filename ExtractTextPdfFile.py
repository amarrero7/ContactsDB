import PyPDF2
import requests
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def write_text_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    with open(file_path, "r", encoding="utf-8") as file1:
        with open("rcm_farmacia_profiles.txt", "a", encoding='utf-8') as file2:
            for line in file1:
                if (line.find("Publications") != -1): 
                    file2.write("------------------------------------------------------------------" + '\n')
                    break
                if (line != "\n" and not line.startswith(" ")):
                    file2.write(line.strip('\n') + '\n')

with open("rcm_farmacia_profile_pdf_links.txt", "r", encoding="utf-8") as links_file:
    for link in links_file:
        # Download the PDF file
        response = requests.get(link.strip('\n'))
        with open('temp.pdf', 'wb') as file:
            file.write(response.content)

        # Extract text from the downloaded PDF
        extracted_text = extract_text_from_pdf('temp.pdf')

        # Write the extracted text to a file
        write_text_to_file(extracted_text, "output.txt")

        # Remove temp files
        os.remove('temp.pdf')
        os.remove("output.txt")



