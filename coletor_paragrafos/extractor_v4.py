import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

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

    return extracted_paragraphs


def save_to_csv(data, file_path):
    # Save the DataFrame to a CSV file
    data.to_csv(file_path, index=False, encoding='utf-8')


url_list = read_urls_from_file(urls_path)

for url in url_list:
    paragraphs = extract_paragraphs_from_url(url)

    if paragraphs:
        # Create an empty DataFrame to store the data
        df = pd.DataFrame(columns=['URL', 'Paragraph', 'Sentence'])

        for i, paragraph in enumerate(paragraphs):
            # Split the paragraph into sentences
            sentences = re.split("(?<=[.!?])\s+", paragraph)

            # Create a DataFrame for the current paragraph
            temp_df = pd.DataFrame({'URL': [url] * len(sentences), 'Paragraph': [i] * len(sentences), 'Sentence': sentences})

            # Append the DataFrame to the main DataFrame
            df = pd.concat([df, temp_df], ignore_index=True)

        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

        # Construct the file path using the URL
        file_name = url.replace('https://', '').replace('/', '_').replace('www.', '') + '.csv'
        file_path = os.path.join(folder_path, file_name)

        # Save the DataFrame to a CSV file for the current URL
        save_to_csv(df, file_path)
