import os
import csv
import requests
from bs4 import BeautifulSoup
import re

# Example usage
urls_path = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\extracted_urls.txt'
folder_path = 'C:/Users/João Estima/Documents/PROEC/proec_joaoestima/coletor_paragrafos/data/paragraphs_urls'

def read_urls_from_file(urls_path):
    urls = []
    with open(urls_path, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            urls.append(url)
    return urls

def extract_paragraphs_from_url(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the <p> tags in the parsed HTML
    paragraphs = soup.find_all('p')

    extracted_paragraphs = [p.get_text() for p in paragraphs]

    sentences = []

    # Split paragraphs into sentences
    for sentence in extracted_paragraphs:
        sentences += re.split("(?<=[.!?])\s+", sentence)        

    # Extract the text from each <p> tag and store them in a list
    return extracted_paragraphs, sentences


def save_to_csv(paragraphs, sentences, folder, url):
    # Create the folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    # Construct the file path using the URL
    file_name = url.replace('https://', '').replace('/', '_').replace('www.', '') + '.csv'
    file_path = os.path.join(folder, file_name)

    # Open the CSV file in write mode
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Paragraph'])

        # Write each paragraph as a row in the CSV file
        for paragraph in paragraphs:
            writer.writerow([paragraph])
        writer.write(['Paragraph'])    
        for sentence in sentences:
            writer.writerow([sentence])




url_list = read_urls_from_file(urls_path)

for url in url_list:
    paragraphs, senteces = extract_paragraphs_from_url(url)
    save_to_csv(paragraphs, folder_path, url)
