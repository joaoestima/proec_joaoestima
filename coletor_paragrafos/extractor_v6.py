import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

urls_path = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\extracted_urls.txt'
output_folder = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\data_v5'
template_path = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\web_u01_p01.csv'


def read_urls_from_file(urls_path):
    urls = []
    with open(urls_path, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            urls.append(url)
    return urls

def extract_content_from_url(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the <h1> to <h5> tags in the parsed HTML
    title_tags = soup.find_all(re.compile('^h[1-5]$'))

    # Extract the titles
    paragraphs = [title.get_text() for title in title_tags]

    # Find all the <p> tags in the parsed HTML
    paragraph_tags = soup.find_all('p')

    # Extract the paragraphs
    paragraphs += [paragraph.get_text() for paragraph in paragraph_tags]

    return paragraphs

def save_to_csv(data, output_folder, file_name):
    # Save the DataFrame to a CSV file
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, file_name)
    data.to_csv(file_path, index=False, encoding='utf-8')

def main():
    url_list = read_urls_from_file(urls_path)
    for url in url_list:
        paragraphs = extract_content_from_url(url)

        # Create an empty DataFrame to store the data
        df = pd.DataFrame(columns=['URL', 'Paragraph', 'Sentence'])

        # Add titles as separate sentences in the first paragraph
        if paragraphs:
            # Add remaining paragraphs with sentences
            for i, paragraph in enumerate(paragraphs):
                sentences = re.split("(?<=[.!?])\s+", paragraph)

                # Create a DataFrame for the current paragraph
                temp_df = pd.DataFrame({
                    'URL': [url] * len(sentences),
                    'Paragraph': [i] * len(sentences),
                    'Sentence': sentences
                })

                # Append the DataFrame to the main DataFrame
                df = pd.concat([df, temp_df], ignore_index=True)

            # Save the DataFrame to a CSV file for the current URL
            file_name = url.replace('https://', '').replace('/', '_').replace('www.', '') + '.csv'
            save_to_csv(df, output_folder, file_name)
            print(f"Processed: {url}")

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

    print("Merged data saved to data_v4")

main()
