#!/usr/bin/env python3
"""
PDF to Markdown Converter CLI Tool
Converts PDF files to Markdown format
"""

import argparse
import sys
import time
from pathlib import Path
import fitz  # PyMuPDF
from loguru import logger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Logger will be configured in main() based on quiet flag
console = Console()


def pdf_to_markdown(pdf_path, output_path=None, preserve_formatting=True):
    """
    Convert PDF to Markdown
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Path to output Markdown file (optional)
        preserve_formatting: Whether to preserve formatting (headers, lists, etc.)
    
    Returns:
        Markdown content as string, or None on error
    """
    try:
        # Open PDF
        doc = fitz.open(pdf_path)
        markdown_content = []
        
        # Extract metadata
        metadata = doc.metadata
        if metadata.get('title'):
            markdown_content.append(f"# {metadata['title']}\n\n")
        if metadata.get('author'):
            markdown_content.append(f"**Author:** {metadata['author']}\n\n")
        if metadata.get('subject'):
            markdown_content.append(f"**Subject:** {metadata['subject']}\n\n")
        
        markdown_content.append("---\n\n")
        
        # Process each page
        for page_num, page in enumerate(doc, start=1):
            if preserve_formatting:
                # Try to extract structured content
                blocks = page.get_text("dict")
                
                for block in blocks["blocks"]:
                    if "lines" in block:  # Text block
                        paragraph = []
                        for line in block["lines"]:
                            line_text = []
                            for span in line["spans"]:
                                text = span["text"]
                                flags = span["flags"]
                                
                                # Apply formatting based on font flags
                                if flags & 2**4:  # Bold
                                    text = f"**{text}**"
                                if flags & 2**1:  # Italic
                                    text = f"*{text}*"
                                
                                line_text.append(text)
                            
                            if line_text:
                                paragraph.append("".join(line_text))
                        
                        if paragraph:
                            markdown_content.append(" ".join(paragraph) + "\n\n")
            else:
                # Simple text extraction
                text = page.get_text()
                if text.strip():
                    markdown_content.append(text + "\n\n")
            
            # Extract images from page
            if output_path:
                image_list = page.get_images(full=True)
                for img_index, img in enumerate(image_list, start=1):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image_name = f"image_page{page_num}_{img_index}.{image_ext}"
                    image_dir = Path(output_path).parent if Path(output_path).suffix else Path(output_path)
                    image_path = image_dir / image_name
                    image_path.write_bytes(image_bytes)
                    markdown_content.append(f"![{image_name}]({image_name})\n\n")
        
        doc.close()
        
        markdown_text = "".join(markdown_content)
        
        # Save to file if output path provided
        if output_path:
            output_path = Path(output_path)
            output_path.write_text(markdown_text, encoding='utf-8')
            console.print(f"Converted: {pdf_path} → {output_path}", style="bold green")
        
        return markdown_text
    
    except Exception as e:
        logger.error(f"✗ Error converting PDF: {e}")
        return None


def watch_folder(folder_path, output_path=None, preserve_formatting=True):
    """
    Watch a folder for new PDF files and convert them automatically
    
    Args:
        folder_path: Path to folder to watch
        output_path: Output directory for converted files
        preserve_formatting: Whether to preserve formatting
    """
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        logger.error(f"✗ Invalid folder: {folder_path}")
        return
    
    # Set up output directory
    if output_path:
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = folder / "converted"
        output_dir.mkdir(exist_ok=True)
    
    seen_files = set()
    
    # Process existing PDFs first
    logger.info(f"Scanning existing PDFs in {folder}...")
    for pdf_file in folder.glob("*.pdf"):
        seen_files.add(pdf_file)
        output_file = output_dir / f"{pdf_file.stem}.md"
        if not output_file.exists():
            logger.info(f"Converting existing file: {pdf_file.name}")
            result = pdf_to_markdown(pdf_file, output_file, preserve_formatting)
            if result:
                logger.success(f"Converted: {pdf_file.name} → {output_file.name}")
    
    logger.info(f"Watching {folder} for new PDFs... (Press Ctrl+C to stop)")
    
    try:
        while True:
            # Check for new PDF files
            current_files = set(folder.glob("*.pdf"))
            new_files = current_files - seen_files
            
            for pdf_file in new_files:
                # Wait a bit to ensure file is fully written
                time.sleep(1)
                
                if pdf_file.exists() and pdf_file.stat().st_size > 0:
                    seen_files.add(pdf_file)
                    output_file = output_dir / f"{pdf_file.stem}.md"
                    logger.info(f"New PDF detected: {pdf_file.name}")
                    result = pdf_to_markdown(pdf_file, output_file, preserve_formatting)
                    if result:
                        logger.success(f"Converted: {pdf_file.name} → {output_file.name}")
            
            time.sleep(2)  # Check every 2 seconds
            
    except KeyboardInterrupt:
        logger.info("\n🛑 Watch mode stopped")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Convert PDF files to Markdown format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.pdf
  %(prog)s document.pdf -o output.md
  %(prog)s document.pdf --simple
  %(prog)s *.pdf -o output/
  %(prog)s --watch /path/to/folder
        """
    )
    
    parser.add_argument(
        "pdf",
        nargs="*",
        help="PDF file(s) to convert (not needed with --watch)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file or directory (default: same name with .md extension)"
    )
    
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Use simple text extraction (faster, less formatting)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress output"
    )
    
    parser.add_argument(
        "--watch",
        metavar="FOLDER",
        help="Watch a folder for new PDFs and convert them automatically"
    )
    
    args = parser.parse_args()
    
    # Configure logger based on quiet mode
    logger.remove()
    if args.quiet:
        # In quiet mode, only show errors
        logger.add(sys.stderr, level="ERROR", format="<level>{message}</level>")
    else:
        # Normal mode: show info and above with timestamps
        logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")
    
    # Handle watch mode
    if args.watch:
        watch_folder(
            args.watch,
            args.output,
            preserve_formatting=not args.simple
        )
        return 0
    
    # Validate PDF files provided
    if not args.pdf:
        parser.error("PDF file(s) required (or use --watch)")
    
    # Track conversion results
    failed_files = []
    successful_files = []
    
    # Process each PDF file
    for pdf_file in args.pdf:
        pdf_path = Path(pdf_file)
        
        if not pdf_path.exists():
            logger.error(f"File not found: {pdf_path}")
            failed_files.append(pdf_path)
            continue
        
        if not pdf_path.suffix.lower() == '.pdf':
            logger.error(f"Not a PDF file: {pdf_path}")
            failed_files.append(pdf_path)
            continue
        
        # Smart output resolution
        output_candidate = Path(args.output) if args.output else None
        
        if output_candidate and (output_candidate.suffix or len(args.pdf) == 1):
            # Explicit file output, or single file
            output_file = output_candidate if output_candidate.suffix else output_candidate.with_suffix(".md")
            output_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            # Directory mode (explicit dir, multiple files, or glob)
            output_dir = output_candidate or Path(".")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{pdf_path.stem}.md"
        
        if args.verbose and not args.quiet:
            logger.info(f"Converting: {pdf_path} → {output_file}")
        
        # Convert PDF to Markdown with progress spinner (if not quiet)
        if not args.quiet:
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Converting {task.description}"),
                transient=True,
            ) as progress:
                task = progress.add_task(pdf_path.name, total=None)
                
                result = pdf_to_markdown(
                    pdf_path,
                    output_file,
                    preserve_formatting=not args.simple
                )
                
                progress.update(task, completed=True)
        else:
            # Quiet mode - no progress bar
            result = pdf_to_markdown(
                pdf_path,
                output_file,
                preserve_formatting=not args.simple
            )
        
        if result is None:
            logger.error(f"Failed to convert {pdf_path.name}")
            failed_files.append(pdf_path)
        else:
            successful_files.append(pdf_path)
            if not args.quiet:
                logger.success(f"Converted {pdf_path.name}")
    
    # Return appropriate exit code
    if failed_files:
        return 1  # Some files failed
    elif successful_files:
        return 0  # All successful
    else:
        return 1  # No files processed


if __name__ == "__main__":
    sys.exit(main())