from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import os
from tqdm import tqdm
import sys

class COCOAnnotationToMask:
    """
        Directory should be in the structure:

        root_dir/
            annotations.json

            /images
                ... list of images from dataset
            /masks (optional)
            
    """
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.images_dir = os.path.join(self.root_dir, 'images')
        self.coco_client = COCO(os.path.join(self.root_dir, 'annotation.json'))

        # Get the list of filenames that are actually in the images directory
        self.image_filenames_to_process = [f for f in os.listdir(self.images_dir) if f.lower().endswith('.jpg')]
        
        # Create a mapping from filename to image metadata for fast lookup
        self.filename_to_meta = {img['file_name']: img for img in self.coco_client.imgs.values()}

        self.save_dir = root_dir
        if 'masks' not in os.listdir(root_dir):
            os.makedirs(os.path.join(root_dir, 'masks'), exist_ok=True)

    def convert(self):
        no_annotations = 0
        
        # DEBUG: Print the number of images we are about to process
        print(f"DEBUG: Found {len(self.image_filenames_to_process)} images in directory to process.")

        # Iterate through the files ON DISK, not the entire COCO dataset
        pbar = tqdm(self.image_filenames_to_process)

        for filename in pbar:
            try:
                pbar.set_description("{} samples have no annotations".format(no_annotations))
                
                # Get the metadata using our fast lookup
                meta = self.filename_to_meta.get(filename)
                if not meta:
                    print(f"Warning: Could not find metadata for {filename}. Skipping.")
                    continue

                mask = self.generate_mask(meta)
                
                if mask is None:
                    no_annotations += 1
                    continue

                mask = mask.astype(np.uint8)
                output_path = os.path.join(self.save_dir, "masks", f"{meta['file_name']}_mask.npy")
                np.save(output_path, mask)
                
            except Exception as e:
                print(f"Error processing image {filename}: {str(e)}")
                continue
            
    def generate_mask(self, meta):
        try:
            annotation_ids = self.coco_client.getAnnIds(imgIds=meta['id'])
            annotations = self.coco_client.loadAnns(annotation_ids)

            mask = np.zeros((meta['height'], meta['width']), dtype=np.uint8)
            for ann in annotations:
                mask = np.maximum(mask, self.coco_client.annToMask(ann))

            if len(annotations) == 0:
                return None

            return mask
        except Exception as e:
            print(f"Error generating mask for image {meta['id']}: {str(e)}")
            return None

if __name__ == "__main__":
    """
    Example Usage:

        python datasets/converters/cocoAnnotationToMask.py /path/to/data/dir
    """
    if len(sys.argv) < 2:
        print("Usage: python cocoAnnotationToMask.py <root_dir>")
    else:
        root_dir = sys.argv[1]
        converter = COCOAnnotationToMask(root_dir)
        converter.convert()