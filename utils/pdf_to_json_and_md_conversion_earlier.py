# ===============================
# SERIAL PDF → JSON + MARKDOWN
# ===============================

import os
import json
from pathlib import Path
import torch

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser

# ======================================================================
# CONFIGS
# ======================================================================

json_config = {
    "output_format": "json",
    "disable_image_extraction": True,
}

markdown_config = {
    "output_format": "markdown",
    "disable_image_extraction": True,
}

# ======================================================================
# SERIAL WORKER
# ======================================================================

def json_md_worker(pdf_path, json_path, md_path):
    """Convert a single PDF to JSON and Markdown (serial execution)."""

    # -------- JSON pass --------
    json_config_parser = ConfigParser(json_config)
    json_converter = PdfConverter(
        config=json_config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
        processor_list=json_config_parser.get_processors(),
        renderer=json_config_parser.get_renderer(),
    )

    rendered_json_obj = json_converter(pdf_path)
    rendered_json = rendered_json_obj.model_dump()

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rendered_json, f, indent=4, ensure_ascii=False)

    # -------- Markdown pass --------
    md_config_parser = ConfigParser(markdown_config)
    md_converter = PdfConverter(
        config=md_config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
        processor_list=md_config_parser.get_processors(),
        renderer=md_config_parser.get_renderer(),
    )

    rendered_md = md_converter(pdf_path)
    md_text = rendered_md.markdown

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    print(f"✔ Processed: {Path(pdf_path).name}")

# ======================================================================
# SERIAL PIPELINE
# ======================================================================

def convert_pdfs_serial(pdf_folder, json_folder, md_folder):
    os.makedirs(json_folder, exist_ok=True)
    os.makedirs(md_folder, exist_ok=True)

    pdf_files = sorted(
        f for f in os.listdir(pdf_folder)
        if f.lower().endswith(".pdf")
    )

    if not pdf_files:
        raise RuntimeError(f"No PDFs found in {pdf_folder}")

    print(f"\n===== Serial PDF Conversion ({len(pdf_files)} files) =====\n")

    for pdf_name in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_name)
        json_path = os.path.join(json_folder, Path(pdf_name).stem + ".json")
        md_path = os.path.join(md_folder, Path(pdf_name).stem + ".md")

        json_md_worker(pdf_path, json_path, md_path)

    print("\n===== Serial PDF conversion completed =====\n")
