import os
import pandas as pd

urls_path = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\extracted_urls_v5.txt'
output_folder = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data'


def read_urls_from_file(urls_path):
    urls = []
    with open(urls_path, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            urls.append(url)
    return urls


def save_to_csv(data, output_folder, file_name):
    # Save the DataFrame to a CSV file
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, file_name)
    data.to_csv(file_path, index=False, encoding='utf-8')

def main():
    indice = []
    urls = read_urls_from_file(urls_path)
    for i, url in enumerate(urls):
        indice.append(i)
    df = pd.DataFrame(urls)
    df['indice'] = indice
    filename = 'indice_paginas_proec'
    save_to_csv(df, output_folder, filename)
main()

