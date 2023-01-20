[![codecov](https://codecov.io/gh/haddocking/prodigy-cryst/branch/master/graph/badge.svg?token=KCGiAqKRnu)](https://codecov.io/gh/haddocking/prodigy-cryst)

# Interface Classifier

Collection of scripts to predict whether an interface in a protein-protein
complex is biological or crystallographic from its atomic coordinates.

## Quick & Dirty Installation

```bash
git clone http://github.com/biopython/biopython.git
cd biopython
sudo python setup.py install # Alternatively, install locally but fix $PYTHONPATH

wget https://github.com/mittinatten/freesasa/releases/download/1.0/freesasa-1.0.tar.gz
tar -xzvf freesasa-1.0.tar.gz
cd freesasa-1.0
./configure && make && make install

pip3 install scikit-learn==0.22

git clone http://github.com/haddocking/interface-classifier

# Edit the config.py to setup the paths to the freesasa binary and radii files

# Have fun!
```

## Usage

```bash
python interface_classifier.py <pdb file> [--selection <chain1><chain2>]
```

Type --help to get a list of all the possible options of the script.

## Dependencies

- The scripts rely on [Biopython](www.biopython.org) to validate the PDB structures and calculate interatomic distances.
- [freesasa](https://github.com/mittinatten/freesasa), with the parameter set used in NACCESS ([Chothia,1976](http://www.ncbi.nlm.nih.gov/pubmed/994183)), is also required for calculating the buried surface area. Both 2.x and 1.x version series are supported.
- [scikit-learn](https://github.com/scikit-learn/scikit-learn) for Python 3 is necessary to load and use the classifier.

To install and use the scripts, just clone the git repository or download the tarball zip
archive. Make sure `freesasa`, Biopython and scikit-learn are accessible to the Python scripts
through the appropriate environment variables ($PYTHONPATH).

## License

These utilities are open-source and licensed under the Apache License 2.0. For more information
read the LICENSE file.
