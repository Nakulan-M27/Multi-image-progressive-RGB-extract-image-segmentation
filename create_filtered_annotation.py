import os
import json

# Define the paths
train_dir = 'AICrowd/train'
images_dir = os.path.join(train_dir, 'images')
original_annotation_path = os.path.join(train_dir, 'annotation.json')
new_annotation_path = os.path.join(train_dir, 'annotation1.json')

# 1. Get a sorted list of the first 250 image filenames
try:
    image_filenames = sorted(os.listdir(images_dir))
    first_250_filenames = set(image_filenames[:250])
    print(f"Selected the first {len(first_250_filenames)} images from the directory.")
except FileNotFoundError:
    print(f"Error: The directory '{images_dir}' was not found.")
    exit()

# 2. Load the original annotation file
try:
    with open(original_annotation_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("Successfully loaded the original annotation.json.")
except FileNotFoundError:
    print(f"Error: The annotation file '{original_annotation_path}' was not found.")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{original_annotation_path}'. The file may be corrupt.")
    exit()

# 3. Filter the data
# Filter the 'images' list
filtered_images = [img for img in data['images'] if img['file_name'] in first_250_filenames]
print(f"Found {len(filtered_images)} matching image entries in the annotation file.")

# Get the IDs of the filtered images
filtered_image_ids = {img['id'] for img in filtered_images}

# Filter the 'annotations' list
filtered_annotations = [ann for ann in data['annotations'] if ann['image_id'] in filtered_image_ids]
print(f"Found {len(filtered_annotations)} annotations corresponding to these images.")

# 4. Create the new JSON object
new_data = {
    'images': filtered_images,
    'annotations': filtered_annotations,
    'categories': data.get('categories', []) # Use original categories, or an empty list if none
}

# 5. Save the new annotation file
with open(new_annotation_path, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=4)

print(f"\nSuccessfully created '{new_annotation_path}' with data for {len(filtered_images)} images.") 