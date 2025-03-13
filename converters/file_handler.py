"""
File Handler Module
Manages file reading and writing operations for the HEIC to various format converters.
"""
import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
import concurrent.futures
from .image_processor import convert_heic_to_format

# Supported output formats
SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png', 'webp']

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

def get_output_path(input_path: str, output_dir: str, output_format: str) -> str:
    """
    Generate the output file path based on the input HEIC file path.
    
    Args:
        input_path: Path to the input HEIC file
        output_dir: Directory to save the output file
        output_format: Output format extension (jpg, png, webp)
        
    Returns:
        str: Output file path with appropriate extension
    """
    file_name = os.path.basename(input_path)
    name_without_ext = os.path.splitext(file_name)[0]
    return os.path.join(output_dir, f"{name_without_ext}.{output_format.lower()}")

def process_file(input_path: str, output_dir: str, output_format: str, quality: int, 
                preserve_metadata: bool, logger: logging.Logger) -> Dict[str, Any]:
    """
    Process a single HEIC file and convert it to the specified format.
    
    Args:
        input_path: Path to the input HEIC file
        output_dir: Directory to save the output file
        output_format: Output format (jpg, png, webp)
        quality: Output quality (1-100)
        preserve_metadata: Whether to preserve EXIF metadata
        logger: Logger instance
        
    Returns:
        dict: Processing result
    """
    result = {
        "input_path": input_path,
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
        output_path = get_output_path(input_path, output_dir, output_format)
        
        # Convert HEIC to specified format
        logger.info(f"Converting: {input_path} -> {output_path}")
        convert_heic_to_format(
            input_path, 
            output_path, 
            output_format.upper(), 
            quality, 
            preserve_metadata
        )
        
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

def _worker(args: Tuple) -> Dict[str, Any]:
    """
    Worker function for multi-threaded processing.
    
    Args:
        args: Tuple containing (input_path, output_dir, output_format, quality, preserve_metadata, logger)
        
    Returns:
        dict: Processing result
    """
    return process_file(*args)

def process_input(input_path: str, output_dir: str, output_format: str = 'jpg', 
                 quality: int = 90, preserve_metadata: bool = True, 
                 logger: logging.Logger = None, max_workers: int = None) -> Dict[str, Any]:
    """
    Process input file or directory of HEIC files with multi-threading support.
    
    Args:
        input_path: Path to the input file or directory
        output_dir: Directory to save the output files
        output_format: Output format (jpg, png, webp)
        quality: Output quality (1-100)
        preserve_metadata: Whether to preserve EXIF metadata
        logger: Logger instance
        max_workers: Maximum number of worker threads (None = auto)
        
    Returns:
        dict: Processing results summary
    """
    if output_format.lower() not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported output format: {output_format}. "
                         f"Supported formats are: {', '.join(SUPPORTED_FORMATS)}")
    
    results = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "errors": []
    }
    
    # Collect all files to process
    files_to_process = []
    
    # Process a single file
    if os.path.isfile(input_path):
        output_subdir = output_dir
        Path(output_subdir).mkdir(parents=True, exist_ok=True)
        files_to_process.append((input_path, output_subdir, output_format, quality, preserve_metadata, logger))
    
    # Process a directory
    elif os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Calculate relative path to maintain directory structure in output
                rel_path = os.path.relpath(os.path.dirname(file_path), input_path)
                file_output_dir = os.path.join(output_dir, rel_path) if rel_path != '.' else output_dir
                
                # Create output directory if it doesn't exist
                Path(file_output_dir).mkdir(parents=True, exist_ok=True)
                
                # Add to list for batch processing
                files_to_process.append((file_path, file_output_dir, output_format, quality, preserve_metadata, logger))
    
    # Process files using multi-threading
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        file_results = list(executor.map(_worker, files_to_process))
    
    # Compile results
    results["total"] = len(file_results)
    
    for result in file_results:
        if result["success"]:
            results["success"] += 1
        elif result["skipped"]:
            results["skipped"] += 1
        else:
            results["failed"] += 1
            if result["error"]:
                results["errors"].append(f"{result.get('input_path', 'Unknown file')}: {result['error']}")
    
    return results