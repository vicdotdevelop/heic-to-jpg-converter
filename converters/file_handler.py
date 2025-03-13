"""
File Handler Module
Manages file reading and writing operations for the HEIC to JPG converter.
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Any
from .image_processor import convert_heic_to_jpg

def is_heic_file(file_path: str) -> bool:
    """
    Check if a file is a HEIC image based on its extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        bool: True if the file has a HEIC extension, False otherwise
    """
    ext = os.path.splitext(file_path)[1].lower()
    return ext in ['.heic', '.heif']

def get_output_path(input_path: str, output_dir: str) -> str:
    """
    Generate the output JPG file path based on the input HEIC file path.
    
    Args:
        input_path: Path to the input HEIC file
        output_dir: Directory to save the output JPG file
        
    Returns:
        str: Output JPG file path
    """
    file_name = os.path.basename(input_path)
    name_without_ext = os.path.splitext(file_name)[0]
    return os.path.join(output_dir, f"{name_without_ext}.jpg")

def process_file(input_path: str, output_dir: str, quality: int, preserve_metadata: bool, logger: logging.Logger) -> Dict[str, Any]:
    """
    Process a single HEIC file and convert it to JPG.
    
    Args:
        input_path: Path to the input HEIC file
        output_dir: Directory to save the output JPG file
        quality: JPEG quality (1-100)
        preserve_metadata: Whether to preserve EXIF metadata
        logger: Logger instance
        
    Returns:
        dict: Processing result
    """
    result = {
        "success": False,
        "skipped": False,
        "error": None
    }
    
    try:
        # Check if file is a HEIC file
        if not is_heic_file(input_path):
            logger.info(f"Skipping non-HEIC file: {input_path}")
            result["skipped"] = True
            return result
        
        # Get output path
        output_path = get_output_path(input_path, output_dir)
        
        # Convert HEIC to JPG
        logger.info(f"Converting: {input_path} -> {output_path}")
        convert_heic_to_jpg(input_path, output_path, quality, preserve_metadata)
        
        # Check if conversion was successful
        if os.path.exists(output_path):
            logger.info(f"Conversion successful: {output_path}")
            result["success"] = True
        else:
            logger.error(f"Conversion failed: {input_path}")
            result["error"] = f"Output file was not created: {output_path}"
        
    except Exception as e:
        logger.error(f"Error processing file {input_path}: {str(e)}")
        result["error"] = str(e)
    
    return result

def process_input(input_path: str, output_dir: str, quality: int, preserve_metadata: bool, logger: logging.Logger) -> Dict[str, Any]:
    """
    Process input file or directory of HEIC files.
    
    Args:
        input_path: Path to the input file or directory
        output_dir: Directory to save the output JPG files
        quality: JPEG quality (1-100)
        preserve_metadata: Whether to preserve EXIF metadata
        logger: Logger instance
        
    Returns:
        dict: Processing results summary
    """
    results = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "errors": []
    }
    
    # Process a single file
    if os.path.isfile(input_path):
        results["total"] = 1
        result = process_file(input_path, output_dir, quality, preserve_metadata, logger)
        
        if result["success"]:
            results["success"] += 1
        elif result["skipped"]:
            results["skipped"] += 1
        else:
            results["failed"] += 1
            if result["error"]:
                results["errors"].append(result["error"])
    
    # Process a directory
    elif os.path.isdir(input_path):
        file_count = 0
        
        for root, _, files in os.walk(input_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Calculate relative path to maintain directory structure in output
                rel_path = os.path.relpath(os.path.dirname(file_path), input_path)
                file_output_dir = os.path.join(output_dir, rel_path) if rel_path != '.' else output_dir
                
                # Create output directory if it doesn't exist
                Path(file_output_dir).mkdir(parents=True, exist_ok=True)
                
                # Process the file
                result = process_file(file_path, file_output_dir, quality, preserve_metadata, logger)
                file_count += 1
                
                if result["success"]:
                    results["success"] += 1
                elif result["skipped"]:
                    results["skipped"] += 1
                else:
                    results["failed"] += 1
                    if result["error"]:
                        results["errors"].append(f"{file_path}: {result['error']}")
        
        results["total"] = file_count
    
    return results