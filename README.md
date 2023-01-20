[![unittests](https://github.com/haddocking/prodigy-cryst/actions/workflows/unittests.yml/badge.svg)](https://github.com/haddocking/prodigy-cryst/actions/workflows/unittests.yml)
[![codecov](https://codecov.io/gh/haddocking/prodigy-cryst/branch/master/graph/badge.svg?token=KCGiAqKRnu)](https://codecov.io/gh/haddocking/prodigy-cryst)

# PRODIGY-cryst

Collection of scripts to predict whether an interface in a protein-protein complex is biological or crystallographic from its atomic coordinates.

## Installation

```bash
> git clone http://github.com/haddocking/prodigy-cryst
> python setup.py install
```

## Usage

```bash
prodigy_cryst <pdb file> [--selection <chain1><chain2>]
```

Type --help to get a list of all the possible options.
