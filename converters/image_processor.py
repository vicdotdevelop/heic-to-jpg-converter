"""
Image Processing Module
Handles the conversion of HEIC files to JPG format.
"""

import io
import pyheif
import exifread
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS

def extract_metadata(heif_file):
    """
    Extract metadata from a HEIF/HEIC file.
    
    Args:
        heif_file: HEIF file object
        
    Returns:
        dict: Extracted metadata
    """
    metadata = {}
    
    # Get metadata from HEIC image
    for metadata_item in heif_file.metadata or []:
        if metadata_item['type'] == 'Exif':
            exif_stream = io.BytesIO(metadata_item['data'][6:])  # Skip the TIFF header
            exif_tags = exifread.process_file(exif_stream)
            
            for tag in exif_tags:
                metadata[tag] = exif_tags[tag]
    
    return metadata

def apply_metadata(img, metadata):
    """
    Apply metadata to a PIL Image.
    
    Args:
        img: PIL Image object
        metadata: Metadata dictionary
        
    Returns:
        PIL.Image: Image with metadata applied
    """
    if not metadata:
        return img
    
    # Convert exifread tags to PIL Exif format
    exif_dict = {}
    for tag_name, tag_value in metadata.items():
        for tag_id, tag in TAGS.items():
            if tag_name.endswith(tag):
                exif_dict[tag_id] = str(tag_value)
                break
    
    # Save exif data
    if exif_dict:
        exif_bytes = img.info.get('exif', b'')
        img.info['exif'] = exif_bytes
    
    return img

def convert_heic_to_jpg(input_path, output_path, quality=90, preserve_metadata=True):
    """
    Convert a HEIC file to JPG format.
    
    Args:
        input_path: Path to the input HEIC file
        output_path: Path to save the output JPG file
        quality: JPEG quality (1-100)
        preserve_metadata: Whether to preserve EXIF metadata
        
    Returns:
        None
    """
    # Read the HEIC file
    heif_file = pyheif.read(input_path)
    
    # Convert to PIL Image
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    
    # Extract and apply metadata if needed
    if preserve_metadata:
        metadata = extract_metadata(heif_file)
        image = apply_metadata(image, metadata)
    
    # Save as JPG
    image.save(output_path, "JPEG", quality=quality)
    
    return output_path