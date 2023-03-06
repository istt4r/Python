import os
import csv

folder_path = r'C:/Users/jecla/OneDrive/Desktop/FitExport/Standards'
file_list = []

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    # Get the file path
    file_path = os.path.join(folder_path, file_name)
    # Check if the file size is 0KB
    if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
        # Append the file name to the list
        file_list.append(file_name)

# Write the list of file names to a CSV file in the same directory
csv_path = os.path.join(folder_path, 'zero_size_files.txt')
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['File Name'])
    for file_name in file_list:
        writer.writerow([file_name])

print("Done! The list of file names has been written to:", csv_path)
