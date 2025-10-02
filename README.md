# Recoding PDB/CIF B-factor

This script allows you to recode the B-factor column of a PDB/CIF file with any values.

This is useful for using molecular visualisation programs like PyMOL, to color proteins, for example using PyMOL's spectrum function to recolor a protein according to mutational effects.

## Installation

more detailed explanation to be followed

```bash
pip install foobar
```

## Usage
1. Prepare input files
2. Run script
3. Recoloring in PyMOL

## Acknowledgements
Inspired by Professor Tyler Starr, who explained the conceptual approach for recoding B-factors in PDB files with me. This implementation is independently written. I wanted to make a lightweight script that is non-programmer friendly.

I highly recommend looking at [his and Allison Greeney's paper for some impressive figures](https://doi.org/10.1016/j.cell.2020.08.012). He also linked me [their repo which I believe contains all the code they used for the paper, including the figures](https://github.com/jbloomlab/SARS-CoV-2-RBD_DMS/blob/master/results/summary/structure_function.md). 