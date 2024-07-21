import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

urls_path = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\extracted_urls.txt'
output_folder = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\images_data'
template_path = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\web_u01_p01.csv'


def read_urls_from_file(urls_path):
    urls = []
    with open(urls_path, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            urls.append(url)
    return urls


def extract_images_from_url(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the <alt> tags in the parsed HTML
    image_alt = soup.find_all('alt')

    # Extract the paragraphs
    image_alt += [image.get_text() for image in image_alt]

    return image_alt

def save_to_csv(data, output_folder, file_name):
    # Save the DataFrame to a CSV file
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, file_name)
    data.to_csv(file_path, index=False, encoding='utf-8')


def main():
    url_list = read_urls_from_file(urls_path)
    for url in url_list:
        images = extract_images_from_url(url)

        # Create an empty DataFrame to store the data
        df = pd.DataFrame(columns=['URL', 'Paragraph', 'Sentence'])

        # Add titles as separate sentences in the first paragraph
        #if images:
        # Add remaining images with sentences
        for i, image in enumerate(images):
            #sentences = re.split("(?<=[.!?])\s+", image)

            # Create a DataFrame for the current image
            temp_df = pd.DataFrame({
                'URL': [url] * len(image),
                'Image Index': [i] * len(image),
                'Sentence': image
            })

            # Append the DataFrame to the main DataFrame
            df = pd.concat([df, temp_df], ignore_index=True)

        # Save the DataFrame to a CSV file for the current URL
        file_name = url.replace('https://', '').replace('/', '_').replace('www.', '') + 'images_' +'.csv'
        save_to_csv(df, output_folder, file_name)
        print(f"Processed: {url}")

"""
# Merge the generated CSV files with the template
    template_df = pd.read_csv(template_path)

    merged_df = pd.DataFrame(columns=template_df.columns)

    for filename in os.listdir(output_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(output_folder, filename)
            data_df = pd.read_csv(file_path)
            merged_df = pd.concat([merged_df, data_df], ignore_index=True)

    merged_output_path = os.path.join(output_folder, 'merged_data.csv')
    merged_df.to_csv(merged_output_path, index=False, encoding='utf-8')
"""

main()
