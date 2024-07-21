import shutil
import os

# Define the original file names
original_vp9_file = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\estima\SOBRE A PROEC - Proec_files\video\s002_talita.vp9.webm'

# Define the output folder
output_folder = r'C:\Users\joaop\OneDrive\Documents\UNICAMP\PROEC\estima\SOBRE A PROEC - Proec_files\video'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop to create 20 copies
for i in range(3, 257):
    # Format the number with leading zeros
    formatted_number = f'{i:03}'

    # Define the new file names
    new_vp9_file = os.path.join(output_folder, f's{formatted_number}_talita.vp9.webm')

    # Copy the original files to the new file names
    shutil.copyfile(original_vp9_file, new_vp9_file)

print("Files have been successfully copied to the output folder!")
