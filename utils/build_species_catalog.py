"""
Script 1: Build the master species catalog (chemical_species.csv)

This runs extraction + filtering across the ENTIRE dataset (all papers),
collects every distinct raw term that survives filtering, resolves each
one through the manually-resolved CSV and writes one row per unique
resolved species:

    species_id, root_name, synonyms

  - root_name : the resolved/canonical name (clean_label applied),
                 or the normalized raw term itself if unresolved.
  - synonyms  : every distinct raw surface form (as it appeared after
                 filtering, e.g. "co2", "carbon dioxide", "CO2") that
                 mapped to this root, semicolon-separated.

"""

import os
import re
from collections import defaultdict
from pathlib import Path
import argparse

import pandas as pd
from chemdataextractor.doc import Document


### ---- Step 1: Species extraction (identical to original) ---- ###

def read_text_as_bytes(path: Path) -> bytes:
    """
    Read a text file and return bytes (utf-8). ChemDataExtractor.from_string expects bytes.
    """
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    return text.encode("utf-8")


def extract_terms_from_bytes(text_bytes: bytes):
    """
    Create a ChemDataExtractor Document from bytes and return the raw
    chemical entity mention strings (not yet counted/deduplicated).
    """
    doc = Document(text_bytes.decode("utf-8", errors="ignore"))
    return [c.text.strip() for c in doc.cems if getattr(c, "text", "").strip()]


### ---- Step 2: Species filtering ---- ###

def is_reaction_like(term):
    return bool(re.search(r'\+|→|--+|=|•|⇒|←', term)) or len(term) > 15


def is_irrelevant(term):
    t = term.lower()
    if re.search(r'\b(sin|cos|theta|phi|omega|alpha|beta|gamma|mu|nu|pi|rho|tau|lambda|manuscript)\b', t):
        return True
    if re.search(r'[=•→←∑∫∞±′″°ϵϑϕ∂∇ΔΓΛΩΨ]', t):
        return True
    if re.match(r'^\d+[a-zA-Z]', t):
        return True
    if '/' in t and len(t.split('/')) > 2:
        return True
    return False


SUBSCRIPT_MAP = str.maketrans({
    "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
    "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9"
})

CHARGE_PATTERN = re.compile(r'[+\-⁺⁻]')


def normalize_formula(s: str) -> str:
    """
    O₂, O_2, O2+, O2− → O2
    """
    if not s:
        return s
    s = s.replace(" ", "").replace("_", "")
    s = s.translate(SUBSCRIPT_MAP)
    s = CHARGE_PATTERN.sub("", s)
    return s.upper()


JUNK_WORDS = {
    "BOLSIG", "HYDROCARBON", "STAINLESSSTEEL", "QUARTZ",
    "FIGURE", "TABLE", "DATA", "BY"
}


def is_junk(term: str) -> bool:
    return term.upper() in JUNK_WORDS


def filter_term(raw: str):
    raw = raw.strip()

    if is_junk(raw) or is_reaction_like(raw) or is_irrelevant(raw):
        return None

    # CASE 1 — MULTI WORD NAMES
    if " " in raw:
        return raw.lower().strip()

    # CASE 2 — SINGLE WORD NAMES
    if raw.isalpha():
        return raw.lower().strip()

    # CASE 3 — CHEMICAL FORMULAS
    return normalize_formula(raw)


### ---- Step 3: Species Mapping (identical resolution logic) ---- ###

def load_filtered_chemicals(csv_path):
    df = pd.read_csv(csv_path)
    df = df[df["resolved_chemical_name"].notna()]

    # CASE A: "chemical_name" as NAME -> resolved NAME
    name_to_resolved = {
        row["chemical_name"].strip().lower(): row["resolved_chemical_name"].strip().lower()
        for _, row in df.iterrows()
    }

    # CASE B: "chemical_name" as FORMULA (CO2, O2, etc.)
    formula_to_resolved = {
        normalize_formula(row["chemical_name"].strip()): row["resolved_chemical_name"].strip().lower()
        for _, row in df.iterrows()
        if re.fullmatch(r"[A-Z][A-Za-z0-9]*", row["chemical_name"])
    }

    return name_to_resolved, formula_to_resolved


def clean_label(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r"[+\-−]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name


def resolve_term(raw_filtered: str, name2res: dict, form2res: dict) -> str:
    """
    Given a term that has already passed filter_term() (so it is either
    a lowercase multi-word name, a lowercase single-word name, or a
    normalized formula), resolve it to its final root name using the 
    original map_and_aggregate_counts_in_folder().

    Returns the resolved/clean root name (falls back to the
    filtered/normalized term itself if no mapping is found).
    """
    lower = raw_filtered.lower()

    # CASE 1: multi-word name OR CASE 2: single-word alpha name
    if " " in raw_filtered or raw_filtered.isalpha():
        resolved = name2res.get(lower)
        if resolved:
            return clean_label(resolved)
        return lower

    # CASE 3: formula
    norm = normalize_formula(raw_filtered)
    resolved = form2res.get(norm) or name2res.get(lower)
    if resolved:
        return clean_label(resolved)
    return norm.lower()


### ---- Build catalog across the whole dataset ---- ###

def build_species_catalog(raw_txt_folder: str, manually_resolved_csv: str, out_csv: str):
    in_root = Path(raw_txt_folder)
    txt_files = sorted([p for p in in_root.iterdir() if p.suffix.lower() == ".txt"])

    if not txt_files:
        print("No .txt files found in:", in_root)
        return

    name2res, form2res = load_filtered_chemicals(manually_resolved_csv)

    # root_name -> set of distinct raw surface forms seen (synonyms)
    root_to_synonyms = defaultdict(set)

    for txt_path in txt_files:
        print(f"[catalog] Scanning: {txt_path.name}")
        text_bytes = read_text_as_bytes(txt_path)
        raw_terms = extract_terms_from_bytes(text_bytes)

        for raw in raw_terms:
            filtered = filter_term(raw)
            if filtered is None:
                continue

            root = resolve_term(filtered, name2res, form2res)

            # Record the raw filtered surface form as a synonym of the root.
            root_to_synonyms[root].add(filtered)

    # ---- Write catalog ----
    rows = []
    for i, (root, synonyms) in enumerate(sorted(root_to_synonyms.items()), start=1):
        # root itself doesn't need to be repeated inside the synonyms list
        syn_list = sorted(s for s in synonyms if s != root)
        rows.append({
            "species_id": f"SP{i:04d}",
            "root_name": root,
            "synonyms": ";".join(syn_list)
        })

    out_df = pd.DataFrame(rows, columns=["species_id", "root_name", "synonyms"])
    out_df.to_csv(out_csv, index=False)
    print(f"[catalog] Saved: {out_csv} ({len(rows)} unique species)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build master chemical species catalog."
    )

    parser.add_argument(
        "--raw-txt-folder",
        required=True,
        help="Folder containing input .txt files"
    )

    parser.add_argument(
        "--manually-resolved-csv",
        required=True,
        help="Path to manually_resolved.csv"
    )

    parser.add_argument(
        "--output-csv",
        required=True,
        help="Path to output chemical_species.csv"
    )

    args = parser.parse_args()

    build_species_catalog(
        raw_txt_folder=args.raw_txt_folder,
        manually_resolved_csv=args.manually_resolved_csv,
        out_csv=args.output_csv
    )