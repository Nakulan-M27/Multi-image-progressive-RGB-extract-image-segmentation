import os
import json
import shutil

# Define the paths
src_images_dir = r'D:\RBG Footprint imagery\train750\images'
src_annotation_path = r'P:\train\annotation.json'
dst_images_dir = r'AICrowd/train750/images'
dst_annotation_path = r'AICrowd/train750/annotation.json'

# Ensure destination directory exists
os.makedirs(dst_images_dir, exist_ok=True)

# 1. Get the list of image filenames from the source directory
try:
    image_filenames = sorted([f for f in os.listdir(src_images_dir) if f.lower().endswith('.jpg')])
    print(f"Found {len(image_filenames)} images in {src_images_dir}")
except FileNotFoundError:
    print(f"Error: The directory '{src_images_dir}' was not found.")
    exit()

# 2. Copy images to the destination directory
print(f"Copying {len(image_filenames)} images to {dst_images_dir}...")
for img in image_filenames:
    src_path = os.path.join(src_images_dir, img)
    dst_path = os.path.join(dst_images_dir, img)
    shutil.copy2(src_path, dst_path)
print(f"Successfully copied {len(image_filenames)} images")

# 3. Load the original annotation file
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

# 4. Filter the data
# Create a set of image filenames for faster lookup
image_filenames_set = set(image_filenames)

# Filter the 'images' list
filtered_images = [img for img in data['images'] if img['file_name'] in image_filenames_set]
print(f"Found {len(filtered_images)} matching image entries in the annotation file.")

# Get the IDs of the filtered images
filtered_image_ids = {img['id'] for img in filtered_images}

# Filter the 'annotations' list
filtered_annotations = [ann for ann in data['annotations'] if ann['image_id'] in filtered_image_ids]
print(f"Found {len(filtered_annotations)} annotations corresponding to these images.")

# 5. Create the new JSON object
new_data = {
    'images': filtered_images,
    'annotations': filtered_annotations,
    'categories': data.get('categories', [])  # Use original categories, or an empty list if none
}

# 6. Save the new annotation file
with open(dst_annotation_path, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=4)

print(f"\nSuccessfully created '{dst_annotation_path}' with data for {len(filtered_images)} images.")
print(f"Total annotations: {len(filtered_annotations)}")
print(f"Categories: {len(new_data['categories'])}")

# Print some statistics
if filtered_images:
    print(f"\nSample image entries:")
    for i, img in enumerate(filtered_images[:3]):
        print(f"  {i+1}. {img['file_name']} (ID: {img['id']})")
    
    # Count annotations per image
    annotation_counts = {}
    for ann in filtered_annotations:
        image_id = ann['image_id']
        annotation_counts[image_id] = annotation_counts.get(image_id, 0) + 1
    
    if annotation_counts:
        avg_annotations = sum(annotation_counts.values()) / len(annotation_counts)
        print(f"\nAverage annotations per image: {avg_annotations:.2f}")
        print(f"Min annotations per image: {min(annotation_counts.values())}")
        print(f"Max annotations per image: {max(annotation_counts.values())}") 