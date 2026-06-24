import subprocess
import shutil
import pandas as pd
import os
import zipfile
from utils.pdf_to_json_and_md_conversion import convert_pdfs_serial
from utils.md_cleaning import process_md_folders
from utils.md_to_txt_conversion import batch_convert_md_folder
from utils.database_extraction_pipeline import db_processor
from utils.bolsig_extraction_pipeline import bolsig_processor
from utils.country_fetching_pipeline import country_fetch_main
from utils.data_visualisation import generate_all_plots

def prompt_for_species_catalog():
    """
    Asks the user, in main.py's own terminal, whether they have their own
    domain catalog CSV (root_name, synonyms columns) for the species
    extraction step, or want the default chemical catalog built from the
    dataset.
 
    Returns:
        (catalog_csv_path: str, is_chemical_domain: bool)
        catalog_csv_path is "" if the user wants the default chemical
        catalog built automatically (Step7_1) rather than supplying one.
    """
    print("\n=== Species Extraction: domain catalog ===")
    while True:
        ans = input("Do you have your own domain catalog CSV? [y/n]: ").strip().lower()
        if ans in ("y", "yes"):
            has_own = True
            break
        if ans in ("n", "no"):
            has_own = False
            break
        print("Please answer 'y' or 'n'.")
 
    if not has_own:
        print("Using the default chemical species catalog (built from the dataset).")
        return "", True
 
    catalog_csv = input("Enter path to your domain catalog CSV: ").strip()
    if not catalog_csv:
        print("No path entered — falling back to the default chemical catalog.")
        return "", True
 
    while True:
        ans = input("Is this a CHEMICAL domain catalog? [y/n]: ").strip().lower()
        if ans in ("y", "yes"):
            is_chemical = True
            break
        if ans in ("n", "no"):
            is_chemical = False
            break
        print("Please answer 'y' or 'n'.")
 
    return catalog_csv, is_chemical

def write_to_results_excel(sheet_name, dataframe, output_dir="results/data",
                           keep_csv=True, csv_path=None):
    """
    Writes a dataframe into results.xlsx (append sheet).
    Optionally deletes the original CSV.
    """

    # Ensure results folder exists
    os.makedirs(output_dir, exist_ok=True)

    # Excel file path
    excel_path = os.path.join(output_dir, "results.xlsx")

    # Append or create Excel
    if os.path.exists(excel_path):
        with pd.ExcelWriter(excel_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"✔ Added sheet '{sheet_name}' to results.xlsx")

    # DELETE CSV if keep_csv=False
    if csv_path and not keep_csv:
        if os.path.exists(csv_path):
            os.remove(csv_path)
            print(f"Deleted raw CSV: {csv_path}")
        else:
            print(f"⚠ CSV not found for deletion: {csv_path}")

    # DELETE zip if exists
    zip_path = os.path.join(output_dir, "raw_results.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"🗑 Deleted existing zip file: {zip_path}")


def run_pipeline():

    # Step 1: Convert PDF to MD and JSON
    convert_pdfs_serial(
        pdf_folder="documents/pdfs/",
        json_folder="documents/jsons/",
        md_folder="documents/mds/"
    )

    # Step 2: Md cleaning
    process_md_folders("documents/mds/", "documents/cleaned_mds/")
    
    # Step 3: Convert MDs to TXTs
    batch_convert_md_folder(
        input_root="documents/cleaned_mds/",
        output_root="documents/txts/"
    )

    # Step 4: Database Extraction Pipeline
    db_processor(
        txt_input_dir="documents/txts/",
        author_db_csv="documents/data/author_database.csv",
        output_csv="results/data/Database_counts.csv"
    )

    # Step 5: Bolsig+ Extraction Pipeline
    bolsig_processor(
        txt_input_dir="documents/txts/",
        output_csv="results/data/bolsig+_counts.csv"
    )

    # Step 6: Country Fetching Pipeline
    country_fetch_main(
        input_folder="documents/jsons/",
        output_csv="results/data/country_fetch_outputs.csv"
    )

    # Step 7: Species Extraction Pipeline (Python 3.9 'lxcat_cde' env, for ChemDataExtractor)
    
    catalog_csv, is_chemical_domain = prompt_for_species_catalog()
 
    print("\n\n=== Switching to python 3.9 Gas TM environment ===\n")
 
    # Pass the prompt answers across the env boundary via environment
    # variables, since call_species_extraction.py runs in a separate
    # subprocess/conda env and can't share Python variables directly.
    species_env = os.environ.copy()
    species_env["SPECIES_CATALOG_CSV"] = catalog_csv
    species_env["IS_CHEMICAL_DOMAIN"] = "true" if is_chemical_domain else "false"
 
    subprocess.run([
        "mamba", "run", "-n", "lxcat_cde", "python",
        "utils/call_species_extraction.py"
    ], check=True, env=species_env)

    # Remove intermediate folder
    intermediate_folder = "documents/intermediate/"

    if os.path.exists(intermediate_folder):
        shutil.rmtree(intermediate_folder)
        print(f"Deleted intermediate folder: {intermediate_folder}")
    else:
        print("intermediate folder not found — skipping delete")

    # Storing results

    # Store species extraction result
    gas_csv = "results/data/final_lxcat_species.csv"
    gas_df = pd.read_csv(gas_csv)
    write_to_results_excel(
        sheet_name="Species",
        dataframe=gas_df,
        keep_csv=False,
        csv_path=gas_csv
    )

    # Store database extraction result
    db_csv = "results/data/Database_counts.csv"
    db_df = pd.read_csv(db_csv)
    write_to_results_excel(
        sheet_name="Database",
        dataframe=db_df,
        keep_csv=False,
        csv_path=db_csv
    )

    # Store bolsig+ extraction result
    bs_csv = "results/data/bolsig+_counts.csv"
    bs_df = pd.read_csv(bs_csv)
    write_to_results_excel(
        sheet_name="Bolsig",
        dataframe=bs_df,
        keep_csv=False,
        csv_path=bs_csv
    )

    # Store country fetching result
    ct_csv = "results/data/country_fetch_outputs.csv"
    ct_df = pd.read_csv(ct_csv)
    write_to_results_excel(
        sheet_name="Country",
        dataframe=ct_df,
        keep_csv=False,
        csv_path=ct_csv
    )

    # Step 8: Create Visualisations
    print("\n=== Generating Visualisation Plots ===\n")
    generate_all_plots()

    print("=== Entire Pipeline Completed Successfully!! ===")

if __name__ == "__main__": 
    run_pipeline()
