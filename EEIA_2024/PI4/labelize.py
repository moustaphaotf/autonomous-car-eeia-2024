import os
import csv

def label_images_in_subfolders(data_dir, output_csv):
    images = []
    labels = []
    
    # Traverse through each subfolder
    for label in os.listdir(data_dir):
        label_dir = os.path.join(data_dir, label)
        
        if os.path.isdir(label_dir):  # Ensure it's a directory
            for file in os.listdir(label_dir):
                file_path = os.path.join(label_dir, file)
                
                if os.path.isfile(file_path):  # Ensure it's a file
                    images.append('Images_panneaux/'+label+'/'+file)
                    labels.append(label)
    
    # Write the image paths and labels to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['file_path', 'label'])  # Header row
        for img, lbl in zip(images, labels):
            writer.writerow([img, lbl])

    print(f"Labeling completed. CSV saved to: {output_csv}")

# Example usage
data_dir = 'C:/Users/moustapha/Downloads/Images_panneaux/'  # Replace with the path to your dataset directory
output_csv = 'image_labels.csv'  # Output CSV file name
label_images_in_subfolders(data_dir, output_csv)
