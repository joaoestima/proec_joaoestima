import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

urls_path = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data\extracted_urls_v6.txt'
output_folder = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data\data_v7'
template_path = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data\web_u01_p01.csv'


def read_urls_from_file(urls_path):
    urls = []

    with open(urls_path, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            urls.append(url)
        return urls


def extract_content_from_url(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    tags = soup.find_all(re.compile(r'^h[1-6]$|^b$|^p$|^small$'))
    paragraphs = []
    #sentences = df.drop_duplicates(subset=['Português'], inplace=True)  # Remove duplicate sentences
    for i, tag in enumerate(tags):
        text = tag.get_text().strip()
        if text:
            sentences = re.split("(?<=[.!?])\s+", text)
            for j, sentence in enumerate(sentences):
                paragraphs.append({
                    'URL': url,
                    'Parágrafo': i,
                    'Sentença': j + 1,
                    'Português': sentence.strip(),  # Store only the sentence text
                    'Rev. Português': '',  # Include empty placeholders for other columns
                    'Glosas': '',
                    'Resp. Glosas': '',
                    'Arquivo Vídeo': '',
                    'Resp. Vídeo': '',
                    'Rev. Tradução': '',
                    'Mocap': '',
                    'Vídeo Mocap': '',
                    'Elan': '',
                    'Resp. Elan': '',
                    'Rev. Elan': ''
                })
    paragraphs = pd.DataFrame(paragraphs).drop_duplicates(subset=['Português']).to_dict('records')
    return paragraphs


def save_to_csv(data, output_folder, file_name):
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, file_name)
    df = pd.DataFrame(data)
    df = df[['URL', 'Parágrafo', 'Sentença', 'Português', 'Rev. Português', 'Glosas', 'Resp. Glosas',
             'Arquivo Vídeo', 'Resp. Vídeo', 'Rev. Tradução', 'Mocap', 'Vídeo Mocap', 'Elan', 'Resp. Elan',
             'Rev. Elan']]
    df.to_csv(file_path, index=False, encoding='utf-8')
    df.to_csv(file_path, index=False, encoding='utf-8')


def count_and_store_rows(output_folder):
    total_rows = 0
    for filename in os.listdir(output_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(output_folder, filename)
            data_df = pd.read_csv(file_path)
            total_rows += len(data_df)

    with open(os.path.join(output_folder, 'total_rows.txt'), 'w') as total_rows_file:
        total_rows_file.write(f'Total Rows: {total_rows}')


def main():
    url_list = read_urls_from_file(urls_path)

    try:
        os.makedirs(output_folder)
    except FileExistsError:
        pass  # Output folder already exists

    for j, url in enumerate(url_list):
        paragraphs = extract_content_from_url(url)
        if not paragraphs:
            continue

        df = pd.DataFrame(paragraphs)
        j = len(os.listdir(output_folder)) + 1
        file_name = f'web_u{j}.csv'

        save_to_csv(df, output_folder, file_name)
        print(f"Processed: {url}")

    count_and_store_rows(output_folder)
    print("Row count stored.")


if __name__ == '__main__':
    main()
