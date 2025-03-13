"""
Logger Module
Provides logging functionality for the HEIC to JPG converter.
"""

import logging
import sys
from typing import Dict, Any

def setup_logger():
    """
    Set up and configure the logger.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("heic_converter")
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

def log_summary(logger, results: Dict[str, Any]):
    """
    Log a summary of the conversion process.
    
    Args:
        logger: The logger instance
        results: Dictionary containing conversion results
    """
    logger.info("==== Conversion Summary ====")
    logger.info(f"Total files processed: {results['total']}")
    logger.info(f"Successfully converted: {results['success']}")
    logger.info(f"Failed conversions: {results['failed']}")
    
    if results['skipped'] > 0:
        logger.info(f"Skipped files (non-HEIC): {results['skipped']}")
        
    if results['failed'] > 0 and 'errors' in results:
        logger.info("Errors encountered:")
        for error in results['errors']:
            logger.error(f"  - {error}")
            
    logger.info("============================")