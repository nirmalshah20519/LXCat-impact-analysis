import subprocess

subprocess.run([
        "mamba", "run", "-n", "lxcat_cde", "python",
        "call_species_extraction.py"
    ], check=True)