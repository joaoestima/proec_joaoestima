import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

urls_path = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data\extracted_urls_v6.txt'
output_folder = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data\data_v7'

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
    tags = soup.find_all(re.compile(r'^h[1-6]$|^a$|^p$|^b$|^i$|^small$|^img$|^span$|^ul$|^ol$|^li$|^tr$|^td$'))
    paragraphs = []
    video_counter = 1  # Initialize video counter
    sentence_video_index = {}  # Dictionary to store video index for each unique sentence
    paragraph_index = 0  # Initialize paragraph index

    for tag in tags:
        text = tag.get_text().strip()
        if text:
            sentences = re.split(r"(?<=[.!?:;\n])\s+", text)
            for j, sentence in enumerate(sentences):
                if sentence.strip() not in sentence_video_index:
                    video_index = f"s{video_counter:03d}_talita.vp9.webm"  # Create new video index
                    sentence_video_index[sentence.strip()] = video_index
                    video_counter += 1  # Increment video counter for each new sentence
                else:
                    video_index = sentence_video_index[sentence.strip()]  # Reuse existing video index

                paragraphs.append({
                    'URL': url,
                    'Parágrafo': paragraph_index,
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
                    'Rev. Elan': '',
                    'Video_Index': video_index  # Add video index
                })
            paragraph_index += 1  # Increment paragraph index for each tag with text

    paragraphs = pd.DataFrame(paragraphs).drop_duplicates(subset=['Português']).to_dict('records')
    return paragraphs

def save_to_csv(data, output_folder, file_name):
    os.makedirs(output_folder, exist_ok=True)
    df = pd.DataFrame(data)

    # Reset paragraph indexes to be continuous
    df['Parágrafo'] = pd.factorize(df['Parágrafo'])[0] + 1

    file_path = os.path.join(output_folder, file_name)
    df = df[['URL', 'Parágrafo', 'Sentença', 'Português', 'Rev. Português', 'Glosas', 'Resp. Glosas',
             'Arquivo Vídeo', 'Resp. Vídeo', 'Rev. Tradução', 'Mocap', 'Vídeo Mocap', 'Elan', 'Resp. Elan',
             'Rev. Elan', 'Video_Index']]
    df.to_csv(file_path, index=False, encoding='utf-8')

def count_and_store_rows(output_folder):
    total_rows = 0
    for filename in os.listdir(output_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(output_folder, filename)
            data_df = pd.read_csv(file_path)
            total_rows += len(data_df)

    with open(os.path.join(output_folder, 'total_rows.txt'), 'w') as total_rows_file:
        total_rows_file.write(f'Total linhas: {total_rows}')

def add_accessibility_tags(file_path, output_path, csv_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    tag_pattern = re.compile(r'^h[1-6]$|^a$|^p$|^b$|^i$|^small$|^img$|^span$|^ul$|^ol$|^li$|^tr$|^td$')

    df = pd.read_csv(csv_path)
    video_index_dict = {row['Português']: row['Video_Index'] for index, row in df.iterrows()}

    for tag in soup.find_all(tag_pattern):
        text = tag.get_text().strip()
        if text in video_index_dict:
            video_index = video_index_dict[text]
            tag['class'] = tag.get('class', []) + ['tracked']
            tag['video-name'] = video_index
            print(f"Tag modificada: {tag.name}, Text: {text}, Video: {video_index}")  # Debug log

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f" HTML modificado salvo em: {output_path}")

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
        file_name = f'web_u{j+1}.csv'
        save_to_csv(df, output_folder, file_name)
        print(f"Processado: {url}")

    count_and_store_rows(output_folder)
    print("Contagem de Linhas Salvo no .txt.")

    # Assuming you want to modify a specific HTML file
    html_file_path = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\estima\SOBRE A PROEC - Proec.html'
    output_html_path = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\estima\teste.html'
    csv_path = os.path.join(output_folder, 'web_u1.csv')  # Example, adjust as needed
    add_accessibility_tags(html_file_path, output_html_path, csv_path)

if __name__ == '__main__':
    main()
