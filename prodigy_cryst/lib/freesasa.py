#!/usr/bin/env python
#
# This code is part of the interface classifier tool distribution
# and governed by its license.  Please see the LICENSE file that should
# have been included as part of this package.
#

"""
Functions to execute freesasa and parse its output.
"""

from __future__ import print_function, division

import os
from shutil import ExecError
import subprocess
import sys
import tempfile

try:
    from Bio.PDB import PDBParser
    from Bio.PDB import PDBIO, Select
except ImportError as e:
    print('[!] The interface classifier tool requires Biopython', file=sys.stderr)
    raise ImportError(e)

from ..config import FREESASA_BIN, FREESASA_PAR
from aa_properties import rel_asa


def freesasa_version():
    """
    Parses freesasa version and return two integers corresponding to major and minor
    """
    cmd = '{0} -v'.format(FREESASA_BIN)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    try:
        version_raw = (str(stdout, 'utf-8')).split(os.linesep)[0]
    except ExecError as e:
        # Python 2.7
        print(e)
        version_raw = str(stdout).split(os.linesep)[0]
    version = version_raw.replace("FreeSASA ", "")
    major, minor = version.split(".")[:2]
    return int(major), int(minor)


def execute_freesasa(structure, selection=None):
    """
    Runs the freesasa executable on a PDB file.

    You can get the executable from:
        https://github.com/mittinatten/freesasa
    """
    io = PDBIO()

    # Check FreeSASA installation
    freesasa, param_f = FREESASA_BIN, FREESASA_PAR

    if not os.path.isfile(freesasa):
        raise IOError('[!] freesasa binary not found at `{0}`'.format(freesasa))
    try:
        major, minor = freesasa_version()
    except Exception as e:
        raise IOError(f'[!] error retrieving freesasa version from {freesasa}, {e}')

    if major < 2 and not os.path.isfile(param_f):
        raise IOError('[!] Atomic radii file not found at `{0}`'.format(param_f))

    # Rewrite PDB using Biopython to have a proper format
    # freesasa is very picky with line width (80 characters or fails!)
    # Select chains if necessary
    class ChainSelector(Select):
        def accept_chain(self, chain):
            if selection and chain.id in selection:
                return 1
            elif not selection:
                return 1
            else:
                return 0

    _pdbf = tempfile.NamedTemporaryFile()
    io.set_structure(structure)
    io.save(_pdbf.name, ChainSelector())

    # Run freesasa
    # Save atomic asa output to another temp file
    _outf = tempfile.NamedTemporaryFile()

    if major >= 2:
        cmd = '{0} {1} --format=pdb --radii=naccess -o {2}'.format(
            freesasa, _pdbf.name, _outf.name)
    else:
        cmd = '{0} --B-value-file={1} -c {2} {3}'.format(
            freesasa, _outf.name, param_f, _pdbf.name)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    if p.returncode:
        print('[!] freesasa did not run successfully', file=sys.stderr)
        print(cmd, file=sys.stderr)
        raise Exception(stderr)

    # Rewind & Parse results file
    # Save
    _outf.seek(0)
    asa, rsa = parse_freesasa_output(_outf)

    _pdbf.close()
    _outf.close()

    return asa, rsa


def parse_freesasa_output(fpath):
    """
    Returns per-residue relative accessibility of side-chain and main-chain
    atoms as calculated by freesasa.
    """

    asa_data, rsa_data = {}, {}

    _rsa = rel_asa
    # _bb = set(('CA', 'C', 'N', 'O'))

    P = PDBParser(QUIET=1)
    s = P.get_structure('bogus', fpath.name)
    for res in s.get_residues():
        res_id = (res.parent.id, res.resname, res.id[1])
        _, _, total_asa = 0, 0, 0
        for atom in res:
            aname = atom.name
            at_id = (res.parent.id, res.resname, res.id[1], aname)
            asa = atom.bfactor
            # if atom.name in _bb:
            #     asa_mc += asa
            # else:
            #     asa_sc += asa
            total_asa += asa
            asa_data[at_id] = asa

        rsa_data[res_id] = total_asa / _rsa['total'][res.resname]

    return asa_data, rsa_data
