#!/usr/bin/env python3
"""
md2pdf — Convert Markdown files to PDF.

Usage:
    python md2pdf.py input.md
    python md2pdf.py input.md -o output.pdf
    python md2pdf.py ./docs -o ./output
"""

import os
import sys
from pathlib import Path

import click
import markdown
from pygments.formatters import HtmlFormatter
from weasyprint import HTML, CSS


EXTENSIONS = [
    "extra",        # tables, footnotes, attr_list
    "codehilite",   # syntax highlighting
    "fenced_code",  # ```code blocks```
    "toc",          # table of contents
    "nl2br",        # newlines to <br>
]

EXTENSION_CONFIGS = {
    "codehilite": {
        "css_class": "highlight",
        "guess_lang": False,
    }
}


def get_css() -> str:
    """Load base CSS + pygments syntax highlight CSS."""
    style_path = Path(__file__).parent / "style.css"
    base_css = style_path.read_text(encoding="utf-8") if style_path.exists() else ""
    pygments_css = HtmlFormatter(style="friendly").get_style_defs(".highlight")
    return base_css + "\n" + pygments_css


def md_to_html(md_text: str) -> str:
    """Convert markdown string to HTML string."""
    md = markdown.Markdown(
        extensions=EXTENSIONS,
        extension_configs=EXTENSION_CONFIGS,
    )
    body = md.convert(md_text)
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>{body}</body>
</html>"""


def convert_file(input_path: Path, output_path: Path) -> None:
    """Convert a single .md file to PDF."""
    md_text = input_path.read_text(encoding="utf-8")
    html = md_to_html(md_text)
    css = CSS(string=get_css())
    HTML(string=html, base_url=str(input_path.parent)).write_pdf(
        str(output_path), stylesheets=[css]
    )
    click.echo(f"✓ {input_path} → {output_path}")


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option(
    "-o", "--output",
    default=None,
    help="Output PDF file or directory. Defaults to same location as input.",
)
def main(input_path: str, output: str) -> None:
    """Convert Markdown file(s) to PDF."""
    src = Path(input_path)

    if src.is_file():
        # Single file
        if src.suffix.lower() != ".md":
            click.echo(f"Error: {src} is not a .md file", err=True)
            sys.exit(1)

        if output:
            out = Path(output)
            if out.is_dir():
                out = out / src.with_suffix(".pdf").name
        else:
            out = src.with_suffix(".pdf")

        out.parent.mkdir(parents=True, exist_ok=True)
        convert_file(src, out)

    elif src.is_dir():
        # Batch convert all .md files in directory
        md_files = list(src.rglob("*.md"))
        if not md_files:
            click.echo(f"No .md files found in {src}", err=True)
            sys.exit(1)

        out_dir = Path(output) if output else src
        out_dir.mkdir(parents=True, exist_ok=True)

        for md_file in md_files:
            relative = md_file.relative_to(src)
            out_file = out_dir / relative.with_suffix(".pdf")
            out_file.parent.mkdir(parents=True, exist_ok=True)
            convert_file(md_file, out_file)

        click.echo(f"\nDone. Converted {len(md_files)} file(s).")

    else:
        click.echo(f"Error: {src} is not a file or directory", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
