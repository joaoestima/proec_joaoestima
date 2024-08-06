import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import shutil
from selenium import webdriver

# Caminhos dos arquivos e pastas
urls_path = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data\extracted_urls_v6.txt'
output_folder = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data\data_v7'
component_folder = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data\component'
original_video_file = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\proec_joaoestima\coletor_paragrafos\data\component\video\s001_talita.vp9.webm'

# Função para ler as URLs a partir de um arquivo
def read_urls_from_file(urls_path):
    urls = []
    with open(urls_path, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            urls.append(url)
    return urls

# Função para baixar a página e seus assets usando Selenium
def download_page_with_assets(url, download_folder):
    # Configurando o WebDriver do Selenium
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_folder}  # Define o diretório de download
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    try:
        # Acessando a página
        driver.get(url)
        # Espera para garantir que todos os recursos sejam carregados
        driver.implicitly_wait(10)

        # Salvando a página como "page.html" e baixando os assets
        with open(os.path.join(download_folder, "page.html"), "w", encoding='utf-8') as f:
            f.write(driver.page_source)

        print(f"Página e assets baixados: {url}")
    finally:
        driver.quit()

# Função para extrair o conteúdo de uma página HTML
def extract_content_from_html(file_path, url):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    tags = soup.find_all(re.compile(r'^h[1-6]$|^a$|^p$|^b$|^i$|^small$|^img$|^span$|^ul$|^ol$|^li$|^tr$|^td$'))
    paragraphs = []
    video_counter = 1  # Inicializa o contador de vídeos
    sentence_video_index = {}  # Dicionário para armazenar o índice de vídeo para cada sentença única
    paragraph_index = 0  # Inicializa o índice de parágrafos

    for tag in tags:
        text = tag.get_text().strip()
        if text:
            sentences = re.split(r"(?<=[.!?:;\n])\s+", text)
            for j, sentence in enumerate(sentences):
                if sentence.strip() not in sentence_video_index:
                    video_index = f"s{video_counter:03d}_talita.vp9.webm"  # Cria um novo índice de vídeo
                    sentence_video_index[sentence.strip()] = video_index
                    video_counter += 1  # Incrementa o contador de vídeos para cada nova sentença
                else:
                    video_index = sentence_video_index[sentence.strip()]  # Reutiliza o índice de vídeo existente

                paragraphs.append({
                    'URL': url,  # Salva a URL original
                    'Parágrafo': paragraph_index,
                    'Sentença': j + 1,
                    'Português': sentence.strip(),  # Armazena apenas o texto da sentença
                    'Rev. Português': '',  # Inclui placeholders vazios para outras colunas
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
                    'Video_Index': video_index  # Adiciona o índice de vídeo
                })
            paragraph_index += 1  # Incrementa o índice de parágrafos para cada tag com texto

    paragraphs = pd.DataFrame(paragraphs).drop_duplicates(subset=['Português']).to_dict('records')
    return paragraphs

# Função para adicionar tags de acessibilidade e salvar o HTML modificado
def add_accessibility_tags_and_save_html(html_file_path, output_path, csv_path, assets_folder):
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
            # Se a tag for <p>, remove o atributo 'class' antes de adicionar o 'tracked'
            if tag.name == 'p':
                if 'class' in tag.attrs:
                    del tag['class']  # Remove qualquer classe existente
                tag['class'] = ['tracked']  # Adiciona a classe 'tracked'
            else:
                # Para outras tags, adiciona a classe 'tracked' mantendo as existentes
                tag['class'] = tag.get('class', []) + ['tracked']
            tag['video-name'] = video_index  # Adiciona o atributo 'video-name'
            print(f"Tag modificada: {tag.name}, Text: {text}, Video: {video_index}")  # Log de depuração

    # Adicionar as tags para invocar os componentes no <head>
    head_tag = soup.find('head')
    if head_tag:
        css_link = soup.new_tag('link', rel='stylesheet', href=f'./{assets_folder}/talita.css', media='all', type='text/css')
        js_script = soup.new_tag('script', src=f'./{assets_folder}/talita.js')
        interaction_script = soup.new_tag('script', src=f'./{assets_folder}/talita-text-interaction.css')
        head_tag.append(css_link)
        head_tag.append(js_script)
        head_tag.append(interaction_script)

    # Adicionar o trecho específico ao final do <body>
    body_tag = soup.find('body')
    if body_tag:
        additional_html = f"""
        <link href="./{assets_folder}/talita.css" media="all" rel="stylesheet" type="text/css"/>
        <link href="./{assets_folder}/talita-text-interaction.css" media="all" rel="stylesheet" type="text/css"/>

        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
        <script type="text/javascript" src="./{assets_folder}/talita.js"></script>

        <script src="./{assets_folder}/talita.js" type="text/javascript"></script>
        <script type="text/javascript">
        jQuery(document).ready(function(event){{
            jQuery("body").talita({{
                button:{{ position:"right" }},
                player:{{
                    videoPath:"./{assets_folder}/video/",
                    videoId:"video-name",
                    track:".tracked",
                    width:288,
                    height:324,
                    position:"right"
                }}
            }});
        }});
        </script>
        """
        body_tag.append(BeautifulSoup(additional_html, 'html.parser'))

    # Salvar o HTML modificado
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"HTML modificado salvo em: {output_path}")

# Função para salvar os dados extraídos em um arquivo CSV
def save_to_csv(data, output_folder, file_name):
    os.makedirs(output_folder, exist_ok=True)
    df = pd.DataFrame(data)

    # Resetar os índices de parágrafos para serem contínuos
    df['Parágrafo'] = pd.factorize(df['Parágrafo'])[0] + 1

    file_path = os.path.join(output_folder, file_name)
    df = df[['URL', 'Parágrafo', 'Sentença', 'Português', 'Rev. Português', 'Glosas', 'Resp. Glosas',
             'Arquivo Vídeo', 'Resp. Vídeo', 'Rev. Tradução', 'Mocap', 'Vídeo Mocap', 'Elan', 'Resp. Elan',
             'Rev. Elan', 'Video_Index']]
    df.to_csv(file_path, index=False, encoding='utf-8')

    # Retorna o número de sentenças para criar as cópias de vídeo
    return len(df)

# Função para criar cópias dos vídeos com base no número de sentenças
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
        pass  # O diretório de saída já existe

    for j, url in enumerate(url_list):
        page_folder = os.path.join(output_folder, f'page_{j + 1}')
        os.makedirs(page_folder, exist_ok=True)

        assets_folder = os.path.join(page_folder, f'page_{j + 1}_files')
        os.makedirs(assets_folder, exist_ok=True)

        # Baixar a página e seus assets
        download_page_with_assets(url, assets_folder)

        html_file_path = os.path.join(assets_folder, 'page.html')
        paragraphs = extract_content_from_html(html_file_path, url)  # Passar a URL original para extração de conteúdo
        if not paragraphs:
            continue

        file_name = f'web_u{j + 1}.csv'
        num_sentences = save_to_csv(paragraphs, page_folder, file_name)

        output_html_path = os.path.join(page_folder, 'modified_page.html')
        csv_path = os.path.join(page_folder, file_name)
        add_accessibility_tags_and_save_html(html_file_path, output_html_path, csv_path, f'page_{j + 1}_files')

        # Copiar arquivos CSS e JS para o diretório dos assets
        for component in ['talita.css', 'talita.js', 'talita-text-interaction.css']:
            source_path = os.path.join(component_folder, component)
            destination_path = os.path.join(assets_folder, component)
            if os.path.exists(source_path):
                shutil.copyfile(source_path, destination_path)

        # Criar cópias dos vídeos no diretório apropriado
        video_folder = os.path.join(assets_folder, 'video')
        create_video_copies(num_sentences, video_folder)

    print("Processamento completo.")

if __name__ == '__main__':
    main()
