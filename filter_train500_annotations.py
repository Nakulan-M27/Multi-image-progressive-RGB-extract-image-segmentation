import os
import json
import shutil

# Paths
p_train_annotation = r'P:\train\annotation.json'  # Updated to correct path
train500_images_dir = r'D:\RBG Footprint imagery\train500\images'
output_dir = r'D:\RBG Footprint imagery\train500'
output_annotation_path = os.path.join(output_dir, 'annotation.json')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get list of image filenames in train500
print("Reading image filenames from train500...")
image_files = set(os.listdir(train500_images_dir))
print(f"Found {len(image_files)} images in train500")

# Load the annotation data from P:\train
print("Loading annotation data from P:\\train...")
try:
    with open(p_train_annotation, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("Successfully loaded annotation data")
except FileNotFoundError:
    print(f"Error: Could not find {p_train_annotation}")
    print("Please check if the annotation file exists at P:\\train\\annotation.json")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {p_train_annotation}")
    exit()

# Filter images and annotations
print("Filtering annotations...")
filtered_images = [img for img in data['images'] if img['file_name'] in image_files]
image_ids = set(img['id'] for img in filtered_images)
filtered_annotations = [ann for ann in data['annotations'] if ann['image_id'] in image_ids]

print(f"Found {len(filtered_images)} matching image entries")
print(f"Found {len(filtered_annotations)} corresponding annotations")

# Create filtered data
filtered_data = {
    'images': filtered_images,
    'annotations': filtered_annotations,
    'categories': data.get('categories', [])
}

# Save filtered annotation
print(f"Saving filtered annotation to {output_annotation_path}...")
with open(output_annotation_path, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, indent=4)

print("Done! Filtered annotation saved successfully.")
print(f"Output location: {output_annotation_path}") 