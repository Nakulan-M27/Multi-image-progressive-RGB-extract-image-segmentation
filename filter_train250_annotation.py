import json
import os

# Paths
annotation_path = r'D:\RBG Footprint imagery\train\annotation.json.json'
train250_images_dir = 'AICrowd/train250/images'
output_annotation_path = 'AICrowd/train250/annotation.json'

# Get list of image filenames in train250
image_files = set(os.listdir(train250_images_dir))

# Read annotation.json in a streaming way
with open(annotation_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter images and annotations
filtered_images = [img for img in data['images'] if img['file_name'] in image_files]
image_ids = set(img['id'] for img in filtered_images)
filtered_annotations = [ann for ann in data['annotations'] if ann['image_id'] in image_ids]

# Copy categories as is
filtered_data = {
    'images': filtered_images,
    'annotations': filtered_annotations,
    'categories': data['categories']
}

# Write filtered annotation.json
with open(output_annotation_path, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f)
print(f"Filtered annotation.json written to {output_annotation_path}") 