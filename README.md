# HEIC Image Converter
A tool for macOS that converts HEIC (High-Efficiency Image Container) files to various formats including JPG, PNG, and WebP. The tool is lightweight, efficient, and easy to use, ensuring high-quality output with minimal processing overhead.

## Features
- Convert single HEIC files or entire folders to JPG, PNG, and WebP formats
- Preserve metadata (EXIF data) or optionally disable it
- Adjust output quality
- Multi-threaded batch processing capability for improved performance
- Graphical User Interface (GUI) for easy use
- Handles nested directories
- Comprehensive logging and error handling

## System Requirements
- macOS (latest versions)
- Python 3.9+

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/heic-image-converter.git
   cd heic-image-converter
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### GUI Version
For a user-friendly graphical interface:
```
python gui.py
```

### Command Line
#### Basic Usage
Convert a single HEIC file to JPG:
```
python main.py --input path/to/image.heic
```

Convert an entire folder of HEIC files:
```
python main.py --input path/to/folder
```

#### Advanced Options
Specify an output directory:
```
python main.py --input path/to/image.heic --output path/to/output/directory
```

Choose output format (jpg, jpeg, png, webp):
```
python main.py --input path/to/image.heic --format png
```

Set output quality (1-100, default is 90):
```
python main.py --input path/to/image.heic --quality 85
```

Disable metadata preservation:
```
python main.py --input path/to/image.heic --no-metadata
```

Specify number of processing threads:
```
python main.py --input path/to/folder --threads 4
```

#### Full Command Options
```
python main.py --help
```

This will display all available options:
```
usage: main.py [-h] --input INPUT [--output OUTPUT] [--format FORMAT] [--quality QUALITY] [--no-metadata] [--threads THREADS]

Convert HEIC images to various formats.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Input HEIC file or directory containing HEIC files (default: None)
  --output OUTPUT, -o OUTPUT
                        Output directory (default: same as input)
  --format FORMAT, -f FORMAT
                        Output format. Options: jpg, jpeg, png, webp (default: jpg)
  --quality QUALITY, -q QUALITY
                        Output quality (1-100) (default: 90)
  --no-metadata         Disable metadata preservation (default: False)
  --threads THREADS, -t THREADS
                        Number of processing threads (default: auto)
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
5. **GUI Issues**:
   The GUI requires tkinter, which should be included with your Python installation. If you're having issues, verify that tkinter is properly installed.

## License
This project is licensed under the MIT License - see the LICENSE file for details.