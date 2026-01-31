import re
import os
from pathlib import Path

def filter_markdown(input_filepath, output_filepath):
    """
    Removes tables, fenced equations ($$), and inline math ($) from a Markdown file.
    """

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Input file not found at {input_filepath}")
        return

    # 1. Remove Fenced Equations ($$ ... $$)
    content = re.sub(r'\$\$[\s\S]*?\$\$', '', content, flags=re.MULTILINE)

    # 2. Remove Markdown table separators
    table_separator_pattern = r'^\s*\|(?:-+\s*\|)+\s*$'
    content = re.sub(table_separator_pattern, '', content, flags=re.MULTILINE)

    # 3. Remove Markdown table content
    table_content_pattern = r'^\s*\|.*\|\s*$'
    content = re.sub(table_content_pattern, '', content, flags=re.MULTILINE)

    # 4. Remove Inline Math ($ ... $)
    content = re.sub(r'(?<!\\)\$[^\s$][^$]*(?<!\s)\$', '', content)

    # 5. Remove extra blank lines
    content = re.sub(r'\n\n+', '\n\n', content)

    # Save output
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✔ Cleaned: {input_filepath} → {output_filepath}")

def process_md_folders(root_folder, output_folder):
    """
    Process all Markdown files directly inside root_folder
    and write cleaned files to output_folder.
    """

    root = Path(root_folder)
    out_root = Path(output_folder)
    out_root.mkdir(parents=True, exist_ok=True)

    md_files = list(root.glob("*.md"))

    if not md_files:
        print(f"⚠ No markdown files found in {root_folder}")
        return

    print(f"🧹 Cleaning {len(md_files)} markdown files...")

    for md_path in md_files:
        out_path = out_root / f"{md_path.stem}_cleaned.md"
        filter_markdown(md_path, out_path)
