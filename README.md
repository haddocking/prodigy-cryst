# PRODIGY-cryst

![PyPI - License](https://img.shields.io/pypi/l/prodigy-cryst)
![PyPI - Status](https://img.shields.io/pypi/status/prodigy-cryst)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/prodigy-cryst)
[![ci](https://github.com/haddocking/prodigy-cryst/actions/workflows/ci.yml/badge.svg)](https://github.com/haddocking/prodigy-cryst/actions/workflows/ci.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/4f129d451ec04c4e9529a6eb28457619)](https://www.codacy.com/gh/haddocking/prodigy-cryst/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=haddocking/prodigy-cryst&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/4f129d451ec04c4e9529a6eb28457619)](https://www.codacy.com/gh/haddocking/prodigy-cryst/dashboard?utm_source=github.com&utm_medium=referral&utm_content=haddocking/prodigy-cryst&utm_campaign=Badge_Coverage)
[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B%20%20%E2%97%8B%20%20%E2%97%8B-orange)](https://fair-software.eu)

Collection of scripts to predict whether an interface in a protein-protein complex is biological or crystallographic from its atomic coordinates.

## Installation

```bash
pip install prodigy-cryst
```

## Usage

Type --help to get a list of all the possible options.

```bash
$ prodigy_cryst --help
usage: prodigy_cryst [-h] [--contact_list] [-q] [--selection A B [A,B C ...]] structf

Biological/crystallographic interface classifier based on Intermolecular Contacts (ICs).

positional arguments:
  structf               Structure to analyse in PDB or mmCIF format

optional arguments:
  -h, --help            show this help message and exit
  --contact_list        Output a list of contacts
  -q, --quiet           Outputs only the predicted interface class

Selection Options:

      By default, all intermolecular contacts are taken into consideration,
      a molecule being defined as an isolated group of amino acids sharing
      a common chain identifier. In specific cases, for example
      antibody-antigen complexes, some chains should be considered as a
      single molecule.

      Use the --selection option to provide collections of chains that should
      be considered for the calculation. Separate by a space the chains that
      are to be considered _different_ molecules. Use commas to include multiple
      chains as part of a single group:

      --selection A B => Contacts calculated (only) between chains A and B.
      --selection A,B C => Contacts calculated (only) between chains A and C; and B and C.
      --selection A B C => Contacts calculated (only) between chains A and B; B and C; and A and C.


  --selection A B [A,B C ...]
```

## Examples

Download PDB file 1ppe from the PDB and run the script on it.

```bash
wget https://files.rcsb.org/download/1PPE.pdb
```

Check how PRODIGY-cryst works on the 1PPE.pdb file. The script will output the number of intermolecular contacts, the number of contacts of each type, the link density, and the predicted interface class.

```bash
$ prodigy_cryst 1PPE.pdb
[+] Reading structure file: /home/rodrigo/1PPE.pdb
[+] Selection: E, I
[+] No. of intermolecular contacts: 71
[+] No. of charged-charged contacts: 4
[+] No. of charged-polar contacts: 8
[+] No. of charged-apolar contacts: 24
[+] No. of polar-polar contacts: 0
[+] No. of apolar-polar contacts: 15
[+] No. of apolar-apolar contacts: 20
[+] Link density: 0.14
[+] Class: BIO 0.804 0.196
```
