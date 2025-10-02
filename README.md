# Recoding PDB/CIF B-factor

This script allows you to recode the B-factor column of a PDB/CIF file with any values.

This is useful for using molecular visualisation programs like PyMOL, to color proteins, for example using PyMOL's spectrum function to recolor a protein according to mutational effects.

## Usage
0. Install Python and packages
1. Prepare input files
2. Run script
3. Recoloring in PyMOL

## 0 - Install Python and packages
1. Install Python

https://www.python.org/downloads/windows/

2. Download my github project

[download project](images/1%20download.png)

3. Unzip folder
4. Right-click folder and select "Open in Terminal"

[open in terminal](images/2%20CMD.png)

5. Enter the following into the terminal and press Enter:
```bash
pip install -r requirements.txt
```
[reqs](images/3%20reqs.png)

## 1 - Prepare input files
In the "input" folder, replace "molecule.cif" with your protein of choice. The input has to be named "molecule.cif". You may change this in the .py file if you are not daunted by code.

Similarly, you have to replace the data in the "newvalues.xlsx" file with your own. In the first column put the positions of the amino acid residues whose B-factor you want to change. In the right column, put the value.

[input](images/4%20input.png)

## 2 - Run script
1. Right-click project folder and select "Open in Terminal", like in step 0.4 above
2. Enter the following into the terminal and press Enter:
```bash
python '.\recode B-factors.py'
```
3. The output is in the "output" folder, named "recoded_molecule.cif"

It is a copy of the input, but all B-factors got overwritten with your input data. The unlisted positions get the value "-999.0" by default - this is to help us not color them later in PyMOL.

## 3 - Recoloring in PyMOL
Here I will show how to color the protein, for example with an asymmetric scale.

In this example I mutated an enzyme and got many variants with new reaction speeds. A value of 1 represents no change relative to wild type, 0 would be a dead enzyme, a value of 2 would be double speed relative to wild type and so on. Since there is no upper bound to how much speed a variant can gain, the scale is asymmetric - everything between 0 and 1 is a loss (I will color that with a gradient of blue to white) and everything above 1 is a gain (colored white to red).

I don't want PyMOL to color the positions that I never mutated. These I therefore assigned the B-factor -999, a number outside of that scale.

1. Open recoded_molecule.cif in PyMOL
2. Create selections for coloring by entering this into PyMOL:
```
select untouched, (b = -999.0) 
```
```
select mutation_bad, (b < 1) and not (b = -999.0)
```
```
select mutation_good, ((b = 1) or (b >1)) and not (b = -999.0)
```
[pymol selections](images/5%20pymol%20selections.png)


3. Color
```
color gray70, untouched
```
```
spectrum b, blue_white, mutation_bad, minimum=0, maximum=1
```
```
spectrum b, white_red, mutation_good, minimum=1, maximum=8
```
```
show surface, molecule_recoded
```
[pymol coloring result](images/6%20pymol%20color%20result.png)

## Acknowledgements
Inspired by Professor Tyler Starr, who explained the conceptual approach for recoding B-factors in PDB files to me. This implementation is independently written. I wanted to make a lightweight script that is non-programmer friendly.

I highly recommend looking at [his and Allison Greeney's paper for some impressive figures](https://doi.org/10.1016/j.cell.2020.08.012). He also linked me [their repo which I believe contains all the code they used for the paper, including the figures](https://github.com/jbloomlab/SARS-CoV-2-RBD_DMS/blob/master/results/summary/structure_function.md). 