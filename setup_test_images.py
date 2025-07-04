import os
import shutil
from pathlib import Path

def setup_test_directories():
    """Create necessary test directories if they don't exist."""
    test_dir = os.path.join('AICrowd', 'test')
    images_dir = os.path.join(test_dir, 'images')
    
    # Create directories if they don't exist
    os.makedirs(images_dir, exist_ok=True)
    print(f"Created directory: {images_dir}")
    
    return images_dir

def copy_test_images(source_dir, dest_dir, num_images=100):
    """Copy the first num_images from source directory to destination directory."""
    # Get list of image files
    image_files = [f for f in os.listdir(source_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    # Take only the first num_images
    image_files = sorted(image_files)[:num_images]
    
    # Copy each image
    for image_file in image_files:
        src_path = os.path.join(source_dir, image_file)
        dst_path = os.path.join(dest_dir, image_file)
        shutil.copy2(src_path, dst_path)
        print(f"Copied: {image_file}")
    
    return len(image_files)

def main():
    # Source directory containing test images
    source_dir = r"C:\Users\10h22\OneDrive\Desktop\studies and projects\IITM intern\Programs and algorithms\RGB footprint extract\AIcrowd\test_images"
    
    # Setup test directories
    dest_dir = setup_test_directories()
    
    # Copy test images
    num_copied = copy_test_images(source_dir, dest_dir)
    
    print(f"\nSuccessfully copied {num_copied} test images to {dest_dir}")

if __name__ == "__main__":
    main() 