# PRODIGY-XTAL - Interface Classifier

This is the standalone **PRODIGY-XTAL** (PROtein binDIng enerGY prediction) used to predict whether an interface in a protein-protein complex is **Biological** or **Crystallographic** from its atomic coordinates.

More PRODIGY services are available as web server at https://bianca.science.uu.nl/prodigy/


## Installation
```bash
$ git clone https://github.com/haddocking/prodigy-cryst.git
$ cd prodigy-cryst
$ python setup.py install
```

## Usage

```bash
prodigy_identify <pdb file> [--selection <chain1> <chain2>]
```

Example:
```bash
$ prodigy_identify examples/1ppe.pdb --selection E I

[+] Reading structure file: /Users/rodrigo/repos/prodigy-cryst/examples/1ppe.pdb
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

Type `--help` to get a list of all the possible options of the script.

## Dependencies
* [Biopython](www.biopython.org) to validate the PDB structures and calculate interatomic distances.
* [freesasa](https://github.com/mittinatten/freesasa), with the parameter set used in NACCESS ([Chothia, 1976](http://www.ncbi.nlm.nih.gov/pubmed/994183))
* [scikit-learn](https://github.com/scikit-learn/scikit-learn) to load and use the classifier.


## License
These utilities are open-source and licensed under the Apache License 2.0. For more information read the LICENSE file.

