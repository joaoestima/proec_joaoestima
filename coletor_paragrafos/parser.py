import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import shutil

urls_path = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data\extracted_urls_v6.txt'
output_folder = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data\data_v7'
component_folder = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data\component'
original_video_file = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data\component\video\s001_talita.vp9.webm'


def read_urls_from_file(urls_path):
    urls = []
    with open(urls_path, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            urls.append(url)
    return urls


def download_page(url, output_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(response.text)
    print(f'Página baixada: {url}')


def extract_content_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
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
                    'URL': file_path,
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


def add_accessibility_tags_and_save_html(html_file_path, output_path, csv_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
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

    # Adicionar tags para invocar os componentes
    head_tag = soup.find('head')
    if head_tag:
        css_link = soup.new_tag('link', rel='stylesheet', href='talita.css')
        js_script = soup.new_tag('script', src='talita.js')
        interaction_script = soup.new_tag('script', src='talita-text-interaction.css')
        head_tag.append(css_link)
        head_tag.append(js_script)
        head_tag.append(interaction_script)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"HTML modificado salvo em: {output_path}")


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

    # Retorne o número de sentenças para criar as cópias de vídeo
    return len(df)


def create_video_copies(num_sentences, destination_video_folder):
    os.makedirs(destination_video_folder, exist_ok=True)

    for i in range(1, num_sentences + 1):
        formatted_number = f's{i:03d}_talita.vp9.webm'
        new_video_file = os.path.join(destination_video_folder, formatted_number)
        shutil.copyfile(original_video_file, new_video_file)

    print(f"{num_sentences} cópias de vídeos criadas em: {destination_video_folder}")


def main():
    url_list = read_urls_from_file(urls_path)

    try:
        os.makedirs(output_folder)
    except FileExistsError:
        pass  # Output folder already exists

    for j, url in enumerate(url_list):
        page_folder = os.path.join(output_folder, f'page_{j + 1}')
        os.makedirs(page_folder, exist_ok=True)

        # Diretório para arquivos associados (_files)
        files_folder = os.path.join(page_folder, f'page_{j + 1}_files')
        os.makedirs(files_folder, exist_ok=True)

        html_file_path = os.path.join(page_folder, 'page.html')
        download_page(url, html_file_path)

        paragraphs = extract_content_from_html(html_file_path)
        if not paragraphs:
            continue

        file_name = f'web_u{j + 1}.csv'
        num_sentences = save_to_csv(paragraphs, page_folder, file_name)

        output_html_path = os.path.join(page_folder, 'modified_page.html')
        csv_path = os.path.join(page_folder, file_name)
        add_accessibility_tags_and_save_html(html_file_path, output_html_path, csv_path)

        # Copiar arquivos CSS e JS para o diretório _files
        for component in ['talita.css', 'talita.js', 'talita-text-interaction.js']:
            source_path = os.path.join(component_folder, component)
            destination_path = os.path.join(files_folder, component)
            if os.path.exists(source_path):
                shutil.copyfile(source_path, destination_path)

        # Criar cópias dos vídeos na pasta _files/videos
        video_folder = os.path.join(files_folder, 'videos')
        create_video_copies(num_sentences, video_folder)

    print("Processamento completo.")


if __name__ == '__main__':
    main()
