import os
import csv
import requests
from bs4 import BeautifulSoup

def extract_paragraphs_from_url(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the <p> tags in the parsed HTML
    paragraphs = soup.find_all('p')
    
    # Extract the text from each <p> tag and store them in a list
    extracted_paragraphs = [p.get_text() for p in paragraphs]
    
    return extracted_paragraphs

def save_to_csv(paragraphs, folder, filename):
    # Create the folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)
    
    # Construct the file path
    file_path = os.path.join(folder, filename)
    
    # Open the CSV file in write mode
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write each paragraph as a row in the CSV file
        for paragraph in paragraphs:
            writer.writerow([paragraph])

# Example usage
url = 'https://www.proec.unicamp.br/'  # Replace with the desired URL
folder_path = 'C:/Users/João Estima/Documents/PROEC/proec_joaoestima/coletor_paragrafos/data/'
csv_filename = 'extracted_paragraphs.csv'  # Replace with the desired CSV filename

paragraphs = extract_paragraphs_from_url(url)
save_to_csv(paragraphs, folder_path, csv_filename)