import os
import pandas as pd

data_path = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\paragraphs_url' # Define the folder path containing the CSV files
template_path = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\web_u01_p01.csv'
output_folder = r'C:/Users/João Estima/Documents/PROEC/proec_joaoestima/coletor_paragrafos/data/merged_data'
urls_path = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\extracted_urls.txt'

# Read the template file
template_df = pd.read_csv(template_path)

# Iterate over CSV files in the folder
for filename in os.listdir(data_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(data_path, filename)

        # Read the CSV file
        data_df = pd.read_csv(file_path)

        # Create a new DataFrame with the merged data
        merged_data = pd.DataFrame()
        merged_data['Página'] = data_df['URL']
        merged_data['Parágrafo/Bloco'] = data_df['Paragraph']
        merged_data['Sentença'] = data_df.groupby('Paragraph').cumcount().add(1)
        merged_data['Português'] = data_df['Sentence']

        # Merge the merged_data with the template DataFrame
        merged_df = pd.concat([template_df, merged_data], axis=1)

        # Reset the index to integers
        merged_df.reset_index(drop=True, inplace=True)

        # Create the output file path
        os.makedirs(output_folder, exist_ok=True)
        output_file = filename.replace('.csv', '_merged.csv')
        output_path = os.path.join(output_folder, output_file)

        # Save the merged data to a CSV file
        merged_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Finished: {filename}")
