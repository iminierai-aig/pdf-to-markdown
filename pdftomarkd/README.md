# pdftomarkd

A powerful CLI tool to convert PDF files to Markdown format with automatic image extraction.

## Features

- 📄 Convert PDF files to Markdown format
- 🖼️ Automatic image extraction and embedding
- 📁 Batch processing support
- 👀 Watch mode for automatic conversion
- 🎨 Rich progress bars and colored output
- 🔇 Quiet mode for scripting
- ⚡ Fast and efficient conversion

## Installation

```bash
pip install pdftomarkd
```

Or install from source:

```bash
git clone https://github.com/yourusername/pdftomarkd.git
cd pdftomarkd
pip install .
```

## Usage

### Basic Usage

```bash
# Convert a single PDF file
pdftomarkd document.pdf

# Convert multiple PDFs
pdftomarkd file1.pdf file2.pdf file3.pdf

# Specify output file
pdftomarkd document.pdf -o output.md

# Convert to a directory
pdftomarkd *.pdf -o converted/
```

### Advanced Options

```bash
# Simple text extraction (faster, less formatting)
pdftomarkd document.pdf --simple

# Verbose output
pdftomarkd document.pdf -v

# Quiet mode (suppress output, only show errors)
pdftomarkd document.pdf -q

# Watch a folder for new PDFs
pdftomarkd --watch /path/to/downloads
```

## Examples

```bash
# Convert all PDFs in current directory to markdown/
pdftomarkd *.pdf -o markdown/

# Watch Downloads folder and auto-convert new PDFs
pdftomarkd --watch ~/Downloads

# Convert with custom output directory
pdftomarkd report.pdf -o reports/converted.md
```

## Requirements

- Python 3.8+
- PyMuPDF (fitz)
- loguru
- rich

## License

MIT License

