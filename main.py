#!/usr/bin/env python3
"""
HEIC Image Converter
A command-line tool for macOS that converts HEIC files to various formats.
"""
import sys
import argparse
from converters.cli_interface import parse_args
from converters.file_handler import process_input
from converters.logger import setup_logger, log_summary

def main():
    """Main entry point for the HEIC image converter."""
    # Set up logger
    logger = setup_logger()
    
    try:
        # Parse command line arguments
        args = parse_args()
        
        # Process input (file or directory)
        conversion_results = process_input(
            input_path=args.input,
            output_dir=args.output,
            output_format=args.format,
            quality=args.quality,
            preserve_metadata=not args.no_metadata,
            logger=logger,
            max_workers=args.threads
        )
        
        # Log summary
        log_summary(logger, conversion_results)
        
        return 0
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())