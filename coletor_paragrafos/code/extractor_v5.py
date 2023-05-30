    import os
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    import re

    urls_path = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\extracted_urls.txt'
    folder_path = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\paragraphs_url'
    folder_path_h2 = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\h2_url'


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


    def extract_titles_url(url):
        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the <h2> tags in the parsed HTML
        h2_tags = soup.find_all('h2')

        extracted_h2_tags = [h2.get_text() for h2 in h2_tags]

        return extracted_h2_tags


    def split_paragraphs_into_sentences(paragraphs):
        sentences = []
        for paragraph in paragraphs:
            # Split the paragraph into sentences using regex
            sentences += re.split("(?<=[.!?])\s+", paragraph)
        return sentences


    def save_to_csv(data, folder):
        # Save the DataFrame to a CSV file
        data.to_csv(folder, index=False, encoding='utf-8')


    url_list = read_urls_from_file(urls_path)
    j = 0
    for url in url_list:
        j += 1
        paragraphs = extract_paragraphs_from_url(url)
        h2_tags = extract_titles_url(url)
        #sentences = split_paragraphs_into_sentences(paragraphs)

        if paragraphs:
            # Create an empty DataFrame to store the data
            df = pd.DataFrame(columns=['URL', 'Paragraph', 'Sentence'])
            df_title = pd.DataFrame(columns=['Index', 'Titles'])

            for i, paragraph in enumerate(paragraphs):
                # Split the paragraph into sentences
                sentences = re.split("(?<=[.!?])\s+", paragraph)

                # Create a DataFrame for the current paragraph
                temp_df = pd.DataFrame({
                    'URL': [url] * len(sentences),
                    'Paragraph': [i] * len(sentences),
                    'Sentence': sentences
                })
                # Append the DataFrame to the main DataFrame
                df = pd.concat([df, temp_df], ignore_index=True)

            for k, title in enumerate(h2_tags):
                temp_df_titles = pd.DataFrame({
                    'Index': [k]*len(h2_tags),
                    'Title': title
                })
                df_title = pd.concat([df_title, temp_df_titles], ignore_index=True)
            # Check if the file_path already exists
            os.makedirs(folder_path, exist_ok=True)
            os.makedirs(folder_path_h2, exist_ok=True)

            # Construct the file path using the URL
            file_name = url.replace('https://', '').replace('/', '_').replace('www.', '') + '.csv'
            file_path = os.path.join(folder_path, file_name)
            file_path_h2 = os.path.join(folder_path_h2, file_name)

            # Save the DataFrame to a CSV file for the current URL
            save_to_csv(df, file_path)
            save_to_csv(df_title, file_path_h2)


        print(f"terminado:{url}, processo:{j}")
