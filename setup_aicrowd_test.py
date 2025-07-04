import os
import shutil
from pathlib import Path

def setup_directories():
    """Create necessary directories if they don't exist"""
    dirs = [
        'AICrowd/test/images',
        'AICrowd/test/masks'
    ]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")

def copy_test_files():
    """Copy validation files to test directory"""
    # Source and destination paths
    src_dir = 'AICrowd/val'
    dst_dir = 'AICrowd/test'
    
    # Copy annotation file
    src_ann = os.path.join(src_dir, 'annotation.json')
    dst_ann = os.path.join(dst_dir, 'annotation.json')
    if os.path.exists(src_ann):
        shutil.copy2(src_ann, dst_ann)
        print(f"Copied annotation file to {dst_ann}")
    
    # Copy first 100 images and their masks for testing
    src_img_dir = os.path.join(src_dir, 'images')
    dst_img_dir = os.path.join(dst_dir, 'images')
    src_mask_dir = os.path.join(src_dir, 'masks')
    dst_mask_dir = os.path.join(dst_dir, 'masks')
    
    # Get list of image files
    image_files = sorted(os.listdir(src_img_dir))[:100]  # Take first 100 images
    
    # Copy images and their corresponding masks
    for img_file in image_files:
        # Copy image
        src_img = os.path.join(src_img_dir, img_file)
        dst_img = os.path.join(dst_img_dir, img_file)
        shutil.copy2(src_img, dst_img)
        
        # Copy corresponding mask
        mask_file = f"{img_file}_mask.npy"
        src_mask = os.path.join(src_mask_dir, mask_file)
        dst_mask = os.path.join(dst_mask_dir, mask_file)
        if os.path.exists(src_mask):
            shutil.copy2(src_mask, dst_mask)
    
    print(f"Copied {len(image_files)} images and their masks to test directory")

def main():
    print("Setting up test directory...")
    setup_directories()
    copy_test_files()
    print("Test directory setup complete!")

if __name__ == "__main__":
    main() 