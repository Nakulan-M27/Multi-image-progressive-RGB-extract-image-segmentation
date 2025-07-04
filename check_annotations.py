import os
import json

# Paths
images_dir = 'AICrowd/train/images'
annotation_path = 'AICrowd/train/annotation.json'

# --- 1. Load data ---
# Get the list of actual image files
image_files_on_disk = set(os.listdir(images_dir))

# Load the annotation data
with open(annotation_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# --- 2. Create lookups for efficient checking ---
# Create a set of image IDs that have at least one annotation polygon
annotated_image_ids = {ann['image_id'] for ann in data.get('annotations', [])}

# Create a mapping from image file_name to image_id
filename_to_id = {img['file_name']: img['id'] for img in data.get('images', [])}

# --- 3. Check for annotations ---
annotated_files_found = 0
missing_annotation_files = []

for img_file in image_files_on_disk:
    # Find the image_id for the current file
    image_id = filename_to_id.get(img_file)
    
    # Check if that image_id has any annotations
    if image_id in annotated_image_ids:
        annotated_files_found += 1
    else:
        missing_annotation_files.append(img_file)

# --- 4. Report the results ---
print("--- Annotation Check Report ---")
print(f"Total images in directory: {len(image_files_on_disk)}")
print(f"Images with annotations found in annotation.json: {annotated_files_found}")
print(f"Images MISSING annotations: {len(missing_annotation_files)}")

if missing_annotation_files:
    print("\nFirst 10 images missing annotations:")
    for i, fname in enumerate(missing_annotation_files[:10]):
        print(f" - {fname}")

if annotated_files_found == 0:
    print("\nConclusion: NO images in your directory have corresponding annotations in the JSON file.")
else:
    print("\nConclusion: Some images have annotations, but many do not.") 