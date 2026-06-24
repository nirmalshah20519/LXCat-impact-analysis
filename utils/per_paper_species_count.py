"""
Script 2: Per-paper species counts

This reproduces Steps 1, 2, 4 and 5 of the original pipeline, but
replaces the original Step 3 (re-resolving every raw term against the
manually-resolved CSV inside each paper's loop) with a lookup against a
species catalog (root_name + synonyms), normally the one already built by
01_build_species_catalog.py.

Because the catalog was built using the IDENTICAL filter_term() and
resolve_term() logic as the original Step 3, "raw term -> root_name" is
exactly the same mapping here as in the single-script version. Looking it
up from the catalog instead of recomputing it changes nothing about which
bucket a count lands in, so the per-paper final counts are UNCHANGED for
the chemical-domain path.

---------------------------------------------------------------------------
Domain selection (chemical vs non-chemical)
---------------------------------------------------------------------------
When run from the command line (e.g. via main.py), domain choice is passed
as CLI flags so the whole pipeline stays non-interactive:

    --species-catalog-csv   path to the domain catalog CSV
                             (chemical_species.csv from Script 1, or your own)
    --is-chemical-domain    "true" or "false"

  - is_chemical_domain=True  -> runs exactly the original CDE extraction +
    filtering + catalog-lookup path (Path A below). This is untouched
    from the previously verified version, so chemistry counts are
    guaranteed identical to the original single-script pipeline.

  - is_chemical_domain=False -> ChemDataExtractor is a chemistry NER tool
    and is not meaningful for other domains, so CDE extraction is skipped
    entirely. Instead, every paper's raw text is scanned directly with
    case-insensitive WHOLE-WORD regex matching against every root_name
    and synonym in the catalog (Path B below), and matches are aggregated
    under root_name. This path is only used for non-chemical catalogs and
    never touches/changes the chemical-domain counting logic.

(If you want to be prompted interactively instead — e.g. running this
script by hand — see get_catalog_and_domain() further below; it is not
wired into the CLI entrypoint so unattended pipeline runs never block on
stdin.)

Outputs (per paper):
    Chemical path (Path A) - same as original:
        {file_id}_raw_chem_counts.txt
        {file_id}_filtered_chem_counts.txt
        {file_id}_final_chem_counts_dict.txt
        {file_id}_cde_to_pubchem_mapping.txt

    Non-chemical path (Path B):
        {file_id}_final_chem_counts_dict.txt
        {file_id}_term_match_mapping.txt

Plus the original dataset-level outputs:
    summary_csv          (filename, chemical_counts)
    lxcat_out_csv         (final_lxcat_species.csv)   [chemical path only]

Usage (CLI):
    python utils/Step7_2_per_paper_species_counts.py \
        --raw-txt-folder documents/txts \
        --intermediate-folder documents/intermediate \
        --species-catalog-csv results/data/01_chemical_species.csv \
        --summary-csv documents/species_summary.csv \
        --is-chemical-domain true \
        --lxcat-csv documents/data/LXCat_species_mapping.csv \
        --lxcat-out-dir results/data
"""

import os
import re
import ast
import json
from collections import Counter, defaultdict
from pathlib import Path
import argparse
import pandas as pd
# NOTE: chemdataextractor is only imported lazily, inside the chemical-domain
# path (see extract_and_count_from_bytes), so that this script can still run
# in non-chemical mode on machines where chemdataextractor isn't installed.


### ---- Domain / catalog selection (interactive — for manual/standalone use) ---- ###
#
# NOTE: these helpers are NOT called by the CLI entrypoint at the bottom of
# this file (argparse path). When this script is run via main.py (subprocess,
# unattended), domain choice comes from the --is-chemical-domain CLI flag
# instead, so the pipeline never blocks on stdin. Use get_catalog_and_domain()
# only if you want to run this script manually and be prompted interactively.

def prompt_yes_no(prompt: str) -> bool:
    while True:
        ans = input(f"{prompt} [y/n]: ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")


def get_catalog_and_domain(default_catalog_csv: str = "chemical_species.csv"):
    """
    Ask the user:
      1. Do they have their own domain catalog CSV, or should the default
         chemical_species.csv (from Script 1) be used?
      2. Is the catalog being used a CHEMICAL domain catalog or not?

    Returns:
        catalog_csv_path (str), is_chemical_domain (bool)
    """
    has_own = prompt_yes_no(
        "Do you have your own domain catalog CSV (with root_name & synonyms columns)?"
    )

    if has_own:
        catalog_csv = input("Enter path to your domain catalog CSV: ").strip()
        if not catalog_csv:
            print(f"No path entered, falling back to default: {default_catalog_csv}")
            catalog_csv = default_catalog_csv
    else:
        catalog_csv = default_catalog_csv
        print(f"Using default catalog: {catalog_csv}")

    is_chemical = prompt_yes_no(
        "Is this a CHEMICAL domain catalog (i.e. should ChemDataExtractor be used)?"
    )

    return catalog_csv, is_chemical


### ---- Step 1: Species extraction (identical to original) ---- ###

def read_text_as_bytes(path: Path) -> bytes:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    return text.encode("utf-8")


def extract_and_count_from_bytes(text_bytes: bytes) -> Counter:
    from chemdataextractor.doc import Document  # lazy import: chemical path only
    doc = Document(text_bytes.decode("utf-8", errors="ignore"))
    names = (c.text.strip() for c in doc.cems if getattr(c, "text", "").strip())
    return Counter(names)


def process_all_txts(in_folder: str, out_root: str):
    in_root = Path(in_folder)
    out_root = Path(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    txt_files = sorted([p for p in in_root.iterdir() if p.suffix.lower() == ".txt"])

    if not txt_files:
        print("No .txt files found in:", in_root)
        return

    for txt_path in txt_files:
        file_id = txt_path.stem
        folder = out_root / file_id
        folder.mkdir(parents=True, exist_ok=True)

        print(f"[extract] Processing: {txt_path.name}")

        text_bytes = read_text_as_bytes(txt_path)
        counter = extract_and_count_from_bytes(text_bytes)

        outpath = folder / f"{file_id}_raw_chem_counts.txt"
        with open(outpath, "w", encoding="utf-8") as f:
            for chem, count in counter.most_common():
                f.write(f"{chem}\t{count}\n")

        print(f"[extract] Saved: {outpath}")


### ---- Step 2: Species filtering (identical to original) ---- ###

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


def filter_all_raw_counts(intermediate_root):
    folders = [
        f for f in os.listdir(intermediate_root)
        if os.path.isdir(os.path.join(intermediate_root, f))
    ]

    for folder in folders:
        base = os.path.join(intermediate_root, folder)

        raw_file = os.path.join(base, f"{folder}_raw_chem_counts.txt")
        out_file = os.path.join(base, f"{folder}_filtered_chem_counts.txt")

        if not os.path.exists(raw_file):
            print(f"[filter] Missing raw file for {folder}")
            continue

        filtered = []

        with open(raw_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    chem, count = line.strip().split("\t")
                    count = int(count)
                except Exception:
                    continue

                raw = chem.strip()

                if is_junk(raw) or is_reaction_like(raw) or is_irrelevant(raw):
                    continue

                # CASE 1 — MULTI WORD NAMES
                if " " in raw:
                    filtered.append((raw.lower().strip(), count))
                    continue

                # CASE 2 — SINGLE WORD NAMES
                if raw.isalpha():
                    filtered.append((raw.lower().strip(), count))
                    continue

                # CASE 3 — CHEMICAL FORMULAS
                norm = normalize_formula(raw)
                filtered.append((norm, count))

        with open(out_file, "w", encoding="utf-8") as f:
            for chem, count in sorted(filtered, key=lambda x: -x[1]):
                f.write(f"{chem}\t{count}\n")

        print(f"[filter] {folder}: {len(filtered)} kept")


### ---- Step 3 (replacement): resolve via species catalog lookup ---- ###

def clean_label(name: str) -> str:
    """Kept for parity with the original; catalog root_names are already clean."""
    name = name.lower().strip()
    name = re.sub(r"[+\-−]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name


def load_species_catalog(catalog_csv: str):
    """
    Build a raw-filtered-term -> root_name lookup from the catalog
    produced by 01_build_species_catalog.py.

    The catalog stores, for each root_name, every synonym (raw filtered
    surface form) that resolved to it. We invert that here so each
    individual term -> its root_name, exactly reproducing what
    resolve_term() would have returned for that term in Script 1.
    """
    df = pd.read_csv(catalog_csv)
    df["synonyms"] = df["synonyms"].fillna("")

    term_to_root = {}
    for _, row in df.iterrows():
        root = row["root_name"]
        # the root itself is also a valid raw form (i.e. it resolved to itself)
        term_to_root[root] = root
        for syn in row["synonyms"].split(";"):
            syn = syn.strip()
            if syn:
                term_to_root[syn] = root

    return term_to_root


### ---- Path B: non-chemical domain — regex whole-word counting ---- ###
#
# Used ONLY when the user indicates their catalog is NOT a chemical domain
# catalog. ChemDataExtractor is a chemistry-specific NER tool, so it isn't
# meaningful here. Instead, every root_name and synonym in the catalog is
# matched directly against each paper's raw text using a case-insensitive
# WHOLE-WORD regex, and matches are aggregated under root_name.
#
# This path never runs for, and never affects, the chemical-domain path
# above — it is a fully separate code path.

def build_term_patterns(catalog_csv: str):
    """
    Load a domain catalog (root_name, synonyms) and build, for every
    distinct term (root_name + each synonym), a compiled case-insensitive
    whole-word regex pattern, plus a term -> root_name lookup.

    Multi-word terms are matched as whole phrases (word boundary at the
    start of the first word and the end of the last word), so e.g.
    "cell wall" requires both words to appear together as a phrase.
    """
    df = pd.read_csv(catalog_csv)
    df["synonyms"] = df["synonyms"].fillna("")

    term_to_root = {}
    for _, row in df.iterrows():
        root = str(row["root_name"]).strip()
        if not root:
            continue
        term_to_root[root] = root
        for syn in str(row["synonyms"]).split(";"):
            syn = syn.strip()
            if syn:
                term_to_root[syn] = root

    # Compile longer terms first so overlapping phrases don't get
    # double-counted in a confusing order (e.g. "carbon dioxide" before
    # "carbon"). This only affects iteration order, not whole-word
    # correctness, since each pattern is matched independently.
    terms_sorted = sorted(term_to_root.keys(), key=len, reverse=True)

    term_patterns = []
    for term in terms_sorted:
        escaped = re.escape(term)
        pattern = re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)
        term_patterns.append((term, term_to_root[term], pattern))

    return term_patterns


def count_terms_in_text(text: str, term_patterns) -> Counter:
    """
    Count whole-word, case-insensitive occurrences of each catalog term in
    the given text, returning counts keyed by raw term (not yet aggregated
    to root_name -- that happens in process_all_txts_regex so the mapping
    file can show term -> root explicitly, same spirit as the chemical path).
    """
    counts = Counter()
    for term, root, pattern in term_patterns:
        n = len(pattern.findall(text))
        if n:
            counts[term] = n
    return counts


def process_all_txts_regex(in_folder: str, out_root: str, term_patterns):
    """
    Non-chemical equivalent of process_all_txts + filter_all_raw_counts +
    map_and_aggregate_counts_in_folder combined: for each paper, regex-count
    every catalog term directly in the raw text and aggregate onto
    root_name, writing the same-shaped output files as the chemical path
    (final_chem_counts_dict.txt + a term-mapping file) so create_summary()
    downstream works unchanged.
    """
    in_root = Path(in_folder)
    out_root = Path(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    txt_files = sorted([p for p in in_root.iterdir() if p.suffix.lower() == ".txt"])

    if not txt_files:
        print("No .txt files found in:", in_root)
        return

    for txt_path in txt_files:
        file_id = txt_path.stem
        folder = out_root / file_id
        folder.mkdir(parents=True, exist_ok=True)

        print(f"[regex] Processing: {txt_path.name}")

        with open(txt_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()

        term_counts = count_terms_in_text(text, term_patterns)

        final_counts = defaultdict(int)
        mapping_lines = []

        # Build a quick term -> root lookup from term_patterns for this paper
        term_to_root_local = {term: root for term, root, _ in term_patterns}

        for term, count in term_counts.items():
            root = term_to_root_local[term]
            final_counts[root] += count
            mapping_lines.append(f"{term} => {root}")

        output_dict = folder / f"{file_id}_final_chem_counts_dict.txt"
        output_mapping = folder / f"{file_id}_term_match_mapping.txt"

        with open(output_dict, "w", encoding="utf-8") as out:
            for chem, c in sorted(final_counts.items(), key=lambda x: -x[1]):
                out.write(f"{chem} => {c}\n")

        with open(output_mapping, "w", encoding="utf-8") as m:
            for line in mapping_lines:
                m.write(line + "\n")

        print(f"✅ Folder: {file_id} | Final terms: {len(final_counts)} | Saved → {output_dict}")


def map_and_aggregate_counts_in_folder(intermediate_root, term_to_root: dict):
    subfolders = [
        f for f in os.listdir(intermediate_root)
        if os.path.isdir(os.path.join(intermediate_root, f))
    ]

    for folder in subfolders:
        folder_path = os.path.join(intermediate_root, folder)
        input_file = os.path.join(folder_path, f"{folder}_filtered_chem_counts.txt")
        output_dict = os.path.join(folder_path, f"{folder}_final_chem_counts_dict.txt")
        output_mapping = os.path.join(folder_path, f"{folder}_cde_to_pubchem_mapping.txt")

        if not os.path.exists(input_file):
            print(f"Skipping {folder}: filtered count file not found")
            continue

        final_counts = defaultdict(int)
        mapping_lines = []

        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = re.split(r"\s+", line.strip())
                if len(parts) != 2:
                    continue

                raw_chem, count = parts
                count = int(count)

                # raw_chem here is already the *filtered* term (lowercase
                # name or normalized formula), same as what Script 1's
                # filter_term() produced when building the catalog.
                root = term_to_root.get(raw_chem)

                if root:
                    final_counts[root] += count
                    mapping_lines.append(f"{raw_chem} => {root}")
                else:
                    # Should not normally happen if catalog was built from
                    # the same dataset, but fall back safely just in case
                    # (e.g. catalog built on a subset of papers).
                    fallback = clean_label(raw_chem)
                    final_counts[fallback] += count
                    mapping_lines.append(f"{raw_chem} => [UNRESOLVED] ({fallback})")

        with open(output_dict, "w", encoding="utf-8") as out:
            for chem, c in sorted(final_counts.items(), key=lambda x: -x[1]):
                out.write(f"{chem} => {c}\n")

        with open(output_mapping, "w", encoding="utf-8") as m:
            for line in mapping_lines:
                m.write(line + "\n")

        print(f"✅ Folder: {folder} | Final species: {len(final_counts)} | Saved → {output_dict}")


### ---- Step 4: Species summary (identical to original) ---- ###

def create_summary(intermediate_root, output_csv):
    rows = []

    for folder in sorted(os.listdir(intermediate_root)):
        base = os.path.join(intermediate_root, folder)
        dict_file = os.path.join(base, f"{folder}_final_chem_counts_dict.txt")

        if not os.path.exists(dict_file):
            continue

        chem_dict = {}
        for line in open(dict_file, "r", encoding="utf-8"):
            if "=>" not in line:
                continue
            chem, count = line.split("=>")
            chem_dict[chem.strip()] = int(count.strip())

        rows.append({
            "filename": f"{folder}.txt",
            "chemical_counts": json.dumps(chem_dict)
        })

    pd.DataFrame(rows).to_csv(output_csv, index=False)
    print(f"[summary] Saved: {output_csv}")


### ---- Step 5: LxCat Species Filtering (identical to original) ---- ###

def filter_lxcat_gases(df_path, lxcat_path, out_dir):
    df = pd.read_csv(df_path)
    df["chemical_counts"] = df["chemical_counts"].apply(ast.literal_eval)

    lxcat = pd.read_csv(lxcat_path)
    lxcat_set = set(lxcat['Gas_name'].str.lower().str.strip())

    df["lxcat_gases_count"] = df["chemical_counts"].apply(
        lambda d: {k: v for k, v in d.items() if k.lower() in lxcat_set}
    )

    df = df.drop(['chemical_counts'], axis=1)

    output_dir = Path(out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    out_path = output_dir / "final_lxcat_species.csv"

    df.to_csv(out_path, index=False)
    print(f"[lxcat] Saved: {out_path}")


### ---- Main ---- ###

def run_per_paper_counts(
        raw_txt_folder,
        intermediate_folder,
        species_catalog_csv,
        summary_csv,
        is_chemical_domain=True,
        lxcat_csv=None,
        lxcat_out_dir=None):
    """
    Runs the full per-paper counting pipeline.

    is_chemical_domain=True  -> Path A: identical CDE extraction + filter +
        catalog-lookup logic as the original single-script pipeline.
        Produces guaranteed-identical counts. lxcat_csv and lxcat_out_dir
        are required in this mode (Step 5 LXCat filtering only applies to
        chemical/gas species).

    is_chemical_domain=False -> Path B: ChemDataExtractor is skipped
        entirely (it's chemistry-specific and not meaningful for other
        domains). Instead, every root_name/synonym in the catalog is
        regex-matched (case-insensitive, whole-word) directly against each
        paper's raw text, and matches are aggregated under root_name.
        lxcat_csv/lxcat_out_dir are ignored in this mode since LXCat gas
        filtering doesn't apply to non-chemical domains.
    """

    if is_chemical_domain:
        # ---- Path A: chemical domain (CDE) — unchanged from verified logic ----

        # 1. Extract species (per paper)
        process_all_txts(raw_txt_folder, intermediate_folder)

        # 2. Filter species (per paper)
        filter_all_raw_counts(intermediate_folder)

        # 3. Resolve via species catalog (built by script 1)
        term_to_root = load_species_catalog(species_catalog_csv)
        map_and_aggregate_counts_in_folder(intermediate_folder, term_to_root)

        # 4. Create summary CSV
        create_summary(intermediate_folder, summary_csv)

        # 5. Filter LXCat gases (chemical domain only)
        if not lxcat_csv or not lxcat_out_dir:
            raise ValueError(
                "lxcat_csv and lxcat_out_dir are required when is_chemical_domain=True"
            )
        filter_lxcat_gases(summary_csv, lxcat_csv, lxcat_out_dir)

    else:
        # ---- Path B: non-chemical domain — regex whole-word counting ----

        term_patterns = build_term_patterns(species_catalog_csv)

        # 1-3 combined: regex-extract + aggregate directly per paper
        process_all_txts_regex(raw_txt_folder, intermediate_folder, term_patterns)

        # 4. Create summary CSV (same shape as chemical path)
        create_summary(intermediate_folder, summary_csv)

        # No Step 5 — LXCat gas filtering is chemistry-specific and does
        # not apply to a non-chemical domain catalog.
        print("[info] Non-chemical domain: skipping LXCat gas filtering step.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run per-paper species/term counting pipeline."
    )

    parser.add_argument(
        "--raw-txt-folder",
        required=True,
        help="Folder containing input .txt files"
    )

    parser.add_argument(
        "--intermediate-folder",
        required=True,
        help="Folder for intermediate outputs"
    )

    parser.add_argument(
        "--species-catalog-csv",
        required=True,
        help="Path to the domain catalog CSV (root_name, synonyms columns) "
             "— either chemical_species.csv from script 1, or the user's own."
    )

    parser.add_argument(
        "--summary-csv",
        required=True,
        help="Path to output summary CSV"
    )

    parser.add_argument(
        "--is-chemical-domain",
        required=True,
        choices=["true", "false"],
        help="'true' to use ChemDataExtractor (chemical domain catalog), "
             "'false' to use whole-word regex counting (non-chemical domain catalog)."
    )

    parser.add_argument(
        "--lxcat-csv",
        required=False,
        default=None,
        help="Path to LXCat gas list CSV (required only when --is-chemical-domain=true)"
    )

    parser.add_argument(
        "--lxcat-out-dir",
        required=False,
        default=None,
        help="Directory for final_lxcat_species.csv (required only when --is-chemical-domain=true)"
    )

    args = parser.parse_args()
    is_chemical = args.is_chemical_domain.lower() == "true"

    if is_chemical and (not args.lxcat_csv or not args.lxcat_out_dir):
        parser.error("--lxcat-csv and --lxcat-out-dir are required when --is-chemical-domain=true")

    run_per_paper_counts(
        raw_txt_folder=args.raw_txt_folder,
        intermediate_folder=args.intermediate_folder,
        species_catalog_csv=args.species_catalog_csv,
        summary_csv=args.summary_csv,
        is_chemical_domain=is_chemical,
        lxcat_csv=args.lxcat_csv,
        lxcat_out_dir=args.lxcat_out_dir,
    )