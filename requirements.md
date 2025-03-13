# HEIC to JPG Converter - Requirements Document

## 1. Introduction
### 1.1 Purpose
The **HEIC to JPG Converter** is a command-line tool for macOS that converts HEIC (High-Efficiency Image Container) files to JPG format. The tool aims to be lightweight, efficient, and easy to use, ensuring high-quality output with minimal processing overhead.

### 1.2 Target Audience
- macOS users who need to convert HEIC images to JPG format.
- Developers integrating HEIC to JPG conversion into their workflows.
- Photographers and designers working with Apple devices.

### 1.3 Scope
- Command-line interface (CLI) for batch processing.
- Support for input folder and single-file conversion.
- Retention of metadata (EXIF data).
- Logging and error handling.
- Unit and integration testing.
- Well-documented code with comments and README.

---
## 2. Software Requirements

### 2.1 Functional Requirements
- The software shall take one or more HEIC files as input and convert them to JPG.
- The software shall provide an option to convert an entire folder.
- The software shall preserve metadata (EXIF data) unless explicitly disabled by the user.
- The software shall provide a CLI interface with options:
  - `--input` (specify file or folder)
  - `--output` (specify output directory, default: same as input)
  - `--quality` (set JPEG quality, default: 90%)
  - `--no-metadata` (disable metadata preservation)
- The software shall print conversion progress and errors.
- The software shall handle incorrect input formats gracefully.
- The software shall support batch processing.

### 2.2 Non-Functional Requirements
- The software shall be lightweight and efficient.
- The software shall execute within a reasonable time frame (<2 seconds per file).
- The software shall be compatible with macOS (latest versions).
- The software shall require minimal dependencies.
- The software shall follow proper logging practices.

### 2.3 Dependencies
- Python 3.9+
- `pillow` for image processing
- `pyheif` for HEIC file handling
- `exifread` for metadata extraction

---
## 3. Software Architecture

### 3.1 Architecture Overview
The application follows a modular design with the following components:

- **CLI Interface Module**: Handles command-line input parsing.
- **File Handler Module**: Manages file reading and writing.
- **Image Processing Module**: Converts HEIC to JPG using `pillow` and `pyheif`.
- **Metadata Handler**: Extracts and embeds EXIF metadata using `exifread`.
- **Logger Module**: Provides logging and error handling.
- **Unit Tests**: Ensures functionality across different scenarios.

### 3.2 Process Flow
1. Parse command-line arguments.
2. Validate input (check file/folder existence and HEIC format).
3. Load HEIC files and extract metadata.
4. Convert HEIC to JPG with specified quality.
5. Embed metadata if enabled.
6. Save the converted files to the output directory.
7. Display conversion summary.

---
## 4. Testing Strategy

### 4.1 Unit Testing
- Test CLI argument parsing.
- Test file existence checks.
- Test conversion of a single HEIC file.
- Test conversion of multiple HEIC files.
- Test metadata preservation and removal options.
- Test handling of invalid files.

### 4.2 Integration Testing
- Test batch processing of a directory.
- Test large file conversion performance.
- Test handling of corrupted HEIC files.
- Test output quality validation.

### 4.3 Error Handling Tests
- Missing input files.
- Invalid file formats.
- Permission errors on output directory.

---
## 5. Code Documentation and README

### 5.1 Code Comments
- Each function should have a docstring explaining its purpose.
- Inline comments should be used for complex logic.

### 5.2 README Contents
#### Overview
- Brief description of the tool.

#### Installation
- System requirements.
- Installation steps (including dependencies installation).

#### Usage
- CLI command examples.
- Explanation of optional parameters.

#### Troubleshooting
- Common errors and solutions.

#### License
- Open-source license details.

---
## 6. Deployment and Distribution
- Provide a `requirements.txt` file for dependency installation.
- Optionally package as a standalone macOS app using `pyinstaller`.
- Publish on GitHub with installation and usage instructions.

---
## 7. Future Enhancements
- GUI version using `tkinter` or `PyQt`.
- Support for additional formats (e.g., PNG, WebP).
- Multi-threaded batch processing for performance improvement.

---
### End of Document

