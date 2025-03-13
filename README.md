# HEIC to JPG Converter

A command-line tool for macOS that converts HEIC (High-Efficiency Image Container) files to JPG format. The tool is lightweight, efficient, and easy to use, ensuring high-quality output with minimal processing overhead.

## Features

- Convert single HEIC files or entire folders to JPG format
- Preserve metadata (EXIF data) or optionally disable it
- Adjust JPEG quality
- Batch processing capability
- Handles nested directories
- Comprehensive logging and error handling

## System Requirements

- macOS (latest versions)
- Python 3.9+

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/heic-to-jpg-converter.git
   cd heic-to-jpg-converter
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Convert a single HEIC file:
```
python main.py --input path/to/image.heic
```

Convert an entire folder of HEIC files:
```
python main.py --input path/to/folder
```

### Advanced Options

Specify an output directory:
```
python main.py --input path/to/image.heic --output path/to/output/directory
```

Set JPEG quality (1-100, default is 90):
```
python main.py --input path/to/image.heic --quality 85
```

Disable metadata preservation:
```
python main.py --input path/to/image.heic --no-metadata
```

### Full Command Options

```
python main.py --help
```

This will display all available options:
```
usage: main.py [-h] --input INPUT [--output OUTPUT] [--quality QUALITY] [--no-metadata]

Convert HEIC images to JPG format.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Input HEIC file or directory containing HEIC files (default: None)
  --output OUTPUT, -o OUTPUT
                        Output directory (default: same as input)
  --quality QUALITY, -q QUALITY
                        JPEG quality (1-100) (default: 90)
  --no-metadata         Disable metadata preservation (default: False)
```

## Troubleshooting

### Common Errors

1. **Module not found error**:
   Make sure all dependencies are installed: `pip install -r requirements.txt`

2. **Permission Errors**:
   Ensure you have read/write permissions for the input and output directories.

3. **File Not Found**:
   Verify the path to the input file or directory is correct.

4. **Memory Issues with Large Files**:
   When processing large HEIC files or batches, ensure your system has sufficient memory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.