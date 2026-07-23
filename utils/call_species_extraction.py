"""
Runs inside the 'lxcat_cde' conda env (Python 3.9, ChemDataExtractor).

This is the direct replacement for the old single-pipeline call:

    from species_extraction_pipeline import run_species_extraction_pipeline
    run_species_extraction_pipeline(...)

build_species_catalog.py and per_paper_species_counts.py
each define an argparse CLI in their own `if __name__ == "__main__":`
block, but that block only runs when the file is executed directly. Here
we import the underlying functions instead — build_species_catalog() and
run_per_paper_counts() — and call them with the same keyword arguments
the old single-script pipeline used, so neither Step7_1 nor Step7_2 needs
to be touched or invoked via their own CLI.

Order matters: build_species_catalog() must run first, since
run_per_paper_counts() looks up every term against the catalog it writes.

---------------------------------------------------------------------------
Domain catalog override (set by main.py's interactive prompt)
---------------------------------------------------------------------------
This script runs inside the 'lxcat_cde' subprocess, in a separate
environment from main.py. main.py asks the user, in its own terminal,
whether they have their own domain catalog CSV before launching this
subprocess — but a separate process can't share Python variables
directly, so main.py passes the answer through two environment variables:

    SPECIES_CATALOG_CSV   path to the catalog CSV to use (skips
                           build_species_catalog() entirely if the user
                           supplied their own — see below)
    IS_CHEMICAL_DOMAIN    "true" or "false"

If these are not set (e.g. running this script standalone), it falls
back to the original hardcoded chemical defaults, building the catalog
from the dataset as before.
"""

import os

from build_species_catalog import build_species_catalog
from per_paper_species_count import run_per_paper_counts

RAW_TXT_FOLDER = "documents/txts/"
INTERMEDIATE_FOLDER = "documents/intermediate/"
MANUALLY_RESOLVED_CSV = "documents/manually_resolved.csv"
DEFAULT_SPECIES_CATALOG_CSV = "documents/data/chemical_species.csv"
SUMMARY_CSV = "documents/species_summary.csv"
LXCAT_CSV = "documents/data/LXCat_species_mapping.csv"
LXCAT_OUT_DIR = "results/data"

# ---- Read main.py's prompt answers from the environment ----
user_supplied_catalog = os.environ.get("SPECIES_CATALOG_CSV", "").strip()
is_chemical_domain = os.environ.get("IS_CHEMICAL_DOMAIN", "true").strip().lower() == "true"

if user_supplied_catalog:
    # The user already has their own catalog (root_name, synonyms columns).
    # Skip building one — use it directly in step 2.
    species_catalog_csv = user_supplied_catalog
    print(f"[call_species_extraction] Using user-supplied catalog: {species_catalog_csv}")
else:
    # No catalog supplied: build the default chemical catalog from the
    # dataset, exactly as before.
    species_catalog_csv = DEFAULT_SPECIES_CATALOG_CSV
    print(f"[call_species_extraction] No catalog supplied — building default: {species_catalog_csv}")
    build_species_catalog(
        raw_txt_folder=RAW_TXT_FOLDER,
        manually_resolved_csv=MANUALLY_RESOLVED_CSV,
        out_csv=species_catalog_csv
    )

# Per-paper species/term counts, resolved against species_catalog_csv.
# is_chemical_domain=True keeps this on the original CDE + filter +
# catalog-lookup path, so counts stay identical to the single-script
# pipeline's output. is_chemical_domain=False switches to whole-word
# regex counting (see Step7_2's Path B) and skips LXCat filtering.
run_per_paper_counts(
    raw_txt_folder=RAW_TXT_FOLDER,
    intermediate_folder=INTERMEDIATE_FOLDER,
    species_catalog_csv=species_catalog_csv,
    summary_csv=SUMMARY_CSV,
    is_chemical_domain=is_chemical_domain,
    lxcat_csv=LXCAT_CSV if is_chemical_domain else None,
    lxcat_out_dir=LXCAT_OUT_DIR if is_chemical_domain else None
)