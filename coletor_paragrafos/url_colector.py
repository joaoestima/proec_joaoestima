import os
import requests
from bs4 import BeautifulSoup

page_url = 'https://www.proec.unicamp.br'
file_path = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data'
filename = 'extracted_urls_v1.txt'

def extract_urls_from_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('https://www.proec.unicamp.br/'):
            urls.append(href)
    return urls

def url_writer(extracted_urls, file_path, filename):
    # Create the file_path if it doesn't exist
    os.makedirs(file_path, exist_ok=True)
    # Construct the file path
    file_path = os.path.join(file_path, filename)

    # Write the extracted URLs to a text file
    with open(file_path, 'w', encoding='utf-8') as file:
        for url in extracted_urls:
            file.write(url + '\n')

# Extract URLs from the web page
extracted_urls = extract_urls_from_page(page_url)
url_writer(extracted_urls, file_path, filename)
