# markdown-to-pdf

Convert Markdown files to PDF with a single command. Clean output, supports tables, code blocks, and custom styling.

## Features

- Convert single `.md` file or entire folder
- Syntax highlighting for code blocks
- Table support
- Custom CSS styling
- CLI interface

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Convert single file
python md2pdf.py input.md

# Convert with custom output path
python md2pdf.py input.md -o output.pdf

# Convert all .md files in a folder
python md2pdf.py ./docs -o ./output
```

## Requirements

- Python 3.8+
- See `requirements.txt`

## License

MIT
