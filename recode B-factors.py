import pandas as pd
import os
from pathlib import Path

# --- Define project root
PROJECT_ROOT = Path(__file__).resolve().parent

# --- Input and output paths relative to project root
molecule_path = PROJECT_ROOT / "input" / "molecule.cif"
values_path = PROJECT_ROOT / "input" / "newvalues.xlsx"
output_path = PROJECT_ROOT / "output" / "molecule_recoded.cif"
####output_xlsx = PROJECT_ROOT / "output" / "output_table.xlsx"

# Default B-factor for residues without mutation effect that is to be ignored when coloring
default_bfactor = -999  

# Headers for of pdb
pdb_headers = [
    "Type", "AtomID", "Element", "Atomtype", "Bullet", "Residue", "ChainID", "dontknow1", "ResidueID", "questionmark", "coordX", "coordY", "coordZ", "Occupancy", "Bfactor", "dontknow2", "dontknow3", "dontknow4"
]

# Read molecule.cif and extract ATOM lines
metadata_lines = []
atom_lines = []

with open(molecule_path, 'r') as f:
    for line in f:
        if line.startswith('ATOM'):
            atom_lines.append(line.strip())
        else:
            metadata_lines.append(line.strip())
atom_data = [line.split() for line in atom_lines]
pdbdf = pd.DataFrame(atom_data, columns=pdb_headers)

# Read mutation effects xlsx
mutationeffects = pd.read_excel(values_path)

# Convert convert both to int for merging
pdbdf['ResidueID'] = pdbdf['ResidueID'].astype(int)
mutationeffects['position'] = mutationeffects['position'].astype(int)

# Set default Bfactor for unmutated residues that is to be ignored when coloring
pdbdf['Bfactor'] = default_bfactor
pdbdf = pdbdf.merge(
    mutationeffects[['position', 'effect']],
    left_on='ResidueID',
    right_on='position',
    how='left'
)

# Overwrite Bfactor with 'effect' where available, otherwise keep default Bfactor
pdbdf['Bfactor'] = pdbdf['effect'].fillna(pdbdf['Bfactor'])
pdbdf = pdbdf.drop(columns=['position', 'effect'])


# --- Save outputs ---
####output_xlsx.parent.mkdir(parents=True, exist_ok=True)  
output_path.parent.mkdir(parents=True, exist_ok=True)# ensures that "output" folder exists, makes one otherwise

pdbdf.to_excel(output_xlsx, index=False)

# Write new cif file with updated ATOM lines
with open(output_path, 'w') as f:
    for line in metadata_lines:
        f.write(line + '\n')
    for _, row in pdbdf.iterrows():
        line = ' '.join(row.astype(str))
        f.write(line + '\n')
