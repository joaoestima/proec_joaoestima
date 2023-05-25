import os
import requests
from bs4 import BeautifulSoup
import csv

# Specify the paths and directories
urls_path = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\extracted_urls.txt'
output_directory = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\paragraphs_urls'


def read_urls_from_file(urls_path):
    urls = []
    with open(urls_path, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            urls.append(url)
    return urls

def extract_paragraphs_from_url(url_list, output_directory):
    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        extracted_paragraphs = [p.get_text(strip=True) for p in paragraphs]

        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Create a CSV file for the current URL
        file_name = url.replace('https://www.', '').replace('/', '_') + '.csv'
        file_path = os.path.join(output_directory, file_name)
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['URL', 'Paragraph'])
            for paragraph in extracted_paragraphs:
                writer.writerow([url, paragraph])

# Read the URLs from the file
url_list = read_urls_from_file(urls_path)

# Extract paragraphs from the URLs and save them in separate CSV files
extract_paragraphs_from_url(url_list, output_directory)
