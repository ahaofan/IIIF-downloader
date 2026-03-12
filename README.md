# IIIF Downloader

A Python application for parsing IIIF (International Image Interoperability Framework) format and downloading images with a user-friendly GUI.

## Features

- **JSON Input Support**: Accepts IIIF JSON data directly
- **Automatic Image URL Extraction**: Extracts all high-resolution image URLs from IIIF manifest.json
- **Batch Download**: Downloads all images with progress bar and speed display
- **Work-Named Folders**: Creates folders named after the work for organized storage
- **Default Save Path**: Uses system Downloads folder as default save location
- **Cancel Download**: Allows users to cancel download process at any time
- **User-Friendly Interface**: Clean and intuitive GUI with scrollbars for input/output areas

## System Requirements

- Windows 7 or later
- No Python installation required (standalone executable)

## Usage

1. **Download the executable**: Get the `IIIF-Downloader.exe` from the `dist` folder
2. **Run the application**: Double-click on `IIIF-Downloader.exe`
3. **Input IIIF JSON**: Paste the IIIF JSON data into the input area
4. **Select Save Path**: Choose where to save the downloaded images (default: Downloads folder)
5. **Download Images**: Click "Download All Images" to start downloading
6. **Cancel Download**: Click "Cancel Download" to stop the download process

## How It Works

1. **JSON Parsing**: The application parses the IIIF JSON data to extract image URLs
2. **Image Extraction**: It extracts all high-resolution image URLs from the manifest
3. **Batch Download**: Downloads all images in a separate thread to keep the UI responsive
4. **Progress Tracking**: Displays real-time progress and download speed
5. **Folder Creation**: Creates a folder named after the work to store the downloaded images

## Technical Details

- **Core Technologies**: Python, Tkinter (GUI), Requests (HTTP), tqdm (progress bar)
- **Packaging**: PyInstaller for creating standalone executable
- **Architecture**: Modular design with separate modules for parsing, downloading, and UI

## Development

### Prerequisites

- Python 3.7+
- pip

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd IIIF-downloader

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Packaging

```bash
# Create executable
pyinstaller --onefile --windowed --name IIIF-Downloader main.py

# The executable will be in the dist folder
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [IIIF (International Image Interoperability Framework)](https://iiif.io/)
- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Requests](https://requests.readthedocs.io/)
- [tqdm](https://tqdm.github.io/)