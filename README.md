## pdf-to-markdown ✦

Lightning-fast PDF → clean Markdown converter  
Preserves bold/italic, extracts images, live folder watching

[![PyPI version](https://badge.fury.io/py/pdf-to-markdown.svg)](https://badge.fury.io/py/pdf-to-markdown) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🔤 Preserves bold and italic formatting  
- 🖼️ Extracts and embeds images with relative paths
- 👀 --watch folder mode (auto-convert new PDFs)
- 🎨 Beautiful rich output + progress spinners
- 📦 Batch + glob support (*.pdf)
- ⚡ Zero bloat — lightweight dependencies

## Installation

```
pip install git@https://github.com/iminierai-aig/pdf-to-markdown.git

```
## Usage

```
# Single file
pdftomarkd paper.pdf                     # → paper.md + images/

# Batch mode
pdftomarkd *.pdf -o converted/            # → converted/paper.md + images

# Simple mode (faster, no formatting)
pdftomarkd document.pdf --simple -o output.md

# Watch mode (auto-convert new PDFs)
pdftomarkd --watch ./incoming_pdfs -o ./converted --verbose

# Quiet mode
pdftomarkd bigfile.pdf -q
```

See --help for all flags.

## Demo
Watch the `--watch` mode in action - drop a pdf and see instant conversion!
<iframe src="https://www.loom.com/embed/3c02aefe0a534cfdbd134b8ab91901ae" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>

```
git clone https://github.com/iminierai-aig/pdf-to-markdown.git
cd pdf-to-markdown
pip install -e .
```

Built with using PyMuPDF, loguru, and rich. Contributions welcome!

## License
MIT – see LICENSE
