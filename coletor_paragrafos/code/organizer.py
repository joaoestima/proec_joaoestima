import pandas as pd

def read_paragraphs_from_csv(file_path, column_name):
    df = pd.read_csv(file_path)
    paragraphs = df[column_name].tolist()
    return paragraphs

def update_csv_with_paragraphs(template_file_path, column_name, paragraphs):
    df = pd.read_csv(template_file_path)
    df[column_name] = paragraphs[:len(df)]  # Update the specified column with paragraphs
    df.to_csv(template_file_path, index=False)

# Example usage
template_csv_file = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\web_u01_p01.csv'  # Replace with the path of the CSV file with the template
column_name = r'Português'  # Replace with the desired column name in the template
extracted_csv_file = r'C:\Users\João Estima\Documents\PROEC\proec_joaoestima\coletor_paragrafos\data\extracted_paragraphs.csv'  # Replace with the path of the CSV file containing extracted paragraphs

# Read the extracted paragraphs from the CSV file
paragraphs = read_paragraphs_from_csv(extracted_csv_file, column_name)

# Update the template CSV file with the extracted paragraphs
update_csv_with_paragraphs(template_csv_file, column_name, paragraphs)
