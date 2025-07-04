import os
import json

# Define the paths
src_images_dir = r'D:\RBG Footprint imagery\train1000\images'
src_annotation_path = r'P:\train\annotation.json'
dst_annotation_path = r'D:\RBG Footprint imagery\train1000\images\annotation.json'

# 1. Get the list of image filenames from the source directory
try:
    image_filenames = sorted([f for f in os.listdir(src_images_dir) if f.lower().endswith('.jpg')])
    print(f"Found {len(image_filenames)} images in {src_images_dir}")
except FileNotFoundError:
    print(f"Error: The directory '{src_images_dir}' was not found.")
    exit()

# 2. Load the original annotation file
try:
    with open(src_annotation_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Successfully loaded the original annotation.json from {src_annotation_path}")
except FileNotFoundError:
    print(f"Error: The annotation file '{src_annotation_path}' was not found.")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{src_annotation_path}'. The file may be corrupt.")
    exit()

# 3. Filter the data
image_filenames_set = set(image_filenames)
filtered_images = [img for img in data['images'] if img['file_name'] in image_filenames_set]
print(f"Found {len(filtered_images)} matching image entries in the annotation file.")
filtered_image_ids = {img['id'] for img in filtered_images}
filtered_annotations = [ann for ann in data['annotations'] if ann['image_id'] in filtered_image_ids]
print(f"Found {len(filtered_annotations)} annotations corresponding to these images.")

# 4. Create the new JSON object
new_data = {
    'images': filtered_images,
    'annotations': filtered_annotations,
    'categories': data.get('categories', [])
}

# 5. Save the new annotation file
with open(dst_annotation_path, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=4)

print(f"\nSuccessfully created '{dst_annotation_path}' with data for {len(filtered_images)} images.")
print(f"Total annotations: {len(filtered_annotations)}")
print(f"Categories: {len(new_data['categories'])}") 