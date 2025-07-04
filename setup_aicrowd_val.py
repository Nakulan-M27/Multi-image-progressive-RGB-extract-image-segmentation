import os
import shutil
from pathlib import Path

def setup_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        'AICrowd/val/images',
        'AICrowd/val/masks'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def copy_files():
    """Copy files from source to destination"""
    source_dir = Path(r"C:\Users\10h22\OneDrive\Desktop\studies and projects\IITM intern\Programs and algorithms\RGB footprint extract\AIcrowd\Val")
    dest_dir = Path("AICrowd/val")
    
    # Copy annotation.json
    print("Copying annotation.json...")
    shutil.copy2(source_dir / "annotation.json", dest_dir / "annotation.json")
    
    # Copy images
    print("Copying images...")
    source_images = source_dir / "images"
    dest_images = dest_dir / "images"
    
    # Create destination directory if it doesn't exist
    os.makedirs(dest_images, exist_ok=True)
    
    # Copy all files from source images to destination
    for img_file in source_images.glob("*"):
        if img_file.is_file():
            shutil.copy2(img_file, dest_images / img_file.name)
    
    print("Files copied successfully!")

def main():
    print("Setting up AICrowd validation dataset...")
    
    # Create directories
    setup_directories()
    
    # Copy files
    copy_files()
    
    print("\nSetup complete! The validation dataset is now in the correct location.")
    print("You can now run the processing script to generate masks.")

if __name__ == "__main__":
    main() 