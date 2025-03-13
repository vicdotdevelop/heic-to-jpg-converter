"""
CLI Interface Module
Handles command-line argument parsing for the HEIC to JPG converter.
"""

import os
import argparse
from pathlib import Path

def parse_args():
    """
    Parse command-line arguments for the HEIC to JPG converter.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Convert HEIC images to JPG format.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '--input', '-i', 
        type=str, 
        required=True,
        help='Input HEIC file or directory containing HEIC files'
    )
    
    parser.add_argument(
        '--output', '-o', 
        type=str, 
        help='Output directory (default: same as input)'
    )
    
    parser.add_argument(
        '--quality', '-q', 
        type=int, 
        default=90,
        choices=range(1, 101),
        help='JPEG quality (1-100)'
    )
    
    parser.add_argument(
        '--no-metadata', 
        action='store_true',
        help='Disable metadata preservation'
    )
    
    args = parser.parse_args()
    
    # Validate input path
    if not os.path.exists(args.input):
        raise ValueError(f"Input path does not exist: {args.input}")
    
    # Set default output directory if not provided
    if not args.output:
        if os.path.isdir(args.input):
            args.output = args.input
        else:
            args.output = os.path.dirname(args.input)
    
    # Ensure output directory exists
    Path(args.output).mkdir(parents=True, exist_ok=True)
    
    return args