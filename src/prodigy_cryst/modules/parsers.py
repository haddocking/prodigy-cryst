#!/usr/bin/env python
#
# This code is part of the interface classifier tool distribution
# and governed by its license.  Please see the LICENSE file that should
# have been included as part of this package.
#

"""
Functions to read PDB/mmCIF files
"""

from __future__ import division, print_function

import logging
import os

try:
    from Bio.PDB import MMCIFParser, PDBParser
    from Bio.PDB.Polypeptide import PPBuilder, is_aa
except ImportError as e:
    logging.error("[!] The interface classifier tool requires Biopython")
    raise ImportError(e)


def parse_structure(path):
    """
    Parses a structure using Biopython's PDB/mmCIF Parser
    Verifies the integrity of the structure (gaps) and its
    suitability for the calculation (is it a complex?).
    """
    log = logging.getLogger("Prodigy")
    log.info("[+] Reading structure file: {0}".format(path))
    fname = os.path.basename(path)
    sname = ".".join(fname.split(".")[:-1])
    s_ext = fname.split(".")[-1]

    _ext = set(("pdb", "ent", "cif"))
    if s_ext not in _ext:
        raise IOError(
            "[!] Structure format '{0}' is not supported. Use '.pdb' or '.cif'.".format(
                s_ext
            )
        )

    if s_ext in set(("pdb", "ent")):
        sparser = PDBParser(QUIET=1)
    elif s_ext == "cif":
        sparser = MMCIFParser()

    try:
        s = sparser.get_structure(sname, path)
    except Exception as e:
        # log.error("[!] Structure '{0}' could not be parsed".format(sname))
        log.error("[!] Structure '{0}' could not be parsed".format(sname))
        raise Exception(e)

    # Keep first model only
    if len(s) > 1:
        log.warning(
            "[!] Structure contains more than one model. Only the first one will be kept"
        )
        model_one = s[0].id
        for m in s.child_list[:]:
            if m.id != model_one:
                s.detach_child(m.id)

    # Double occupancy check
    for atom in list(s.get_atoms()):
        if atom.is_disordered():
            residue = atom.parent
            sel_at = atom.selected_child
            sel_at.altloc = " "
            sel_at.disordered_flag = 0
            residue.detach_child(atom.id)
            residue.add(sel_at)

    # Remove HETATMs and solvent
    res_list = list(s.get_residues())

    def _ignore(r):
        return r.id[0][0] == "W" or r.id[0][0] == "H"

    for res in res_list:
        if _ignore(res):
            chain = res.parent
            chain.detach_child(res.id)
        elif not is_aa(res, standard=True):
            raise ValueError(
                "Unsupported non-standard amino acid found: {0}".format(res.resname)
            )
    n_res = len(list(s.get_residues()))

    # Remove Hydrogens
    atom_list = list(s.get_atoms())

    def _ignore(x):
        return x.element == "H"

    for atom in atom_list:
        if _ignore(atom):
            residue = atom.parent
            residue.detach_child(atom.name)

    # Detect gaps and compare with no. of chains
    pep_builder = PPBuilder()
    peptides = pep_builder.build_peptides(s)
    n_peptides = len(peptides)
    n_chains = len(set([c.id for c in s.get_chains()]))

    if n_peptides != n_chains:
        log.warning("[!] Structure contains gaps:")
        for i_pp, pp in enumerate(peptides):
            log.warning(
                "\t{1.parent.id} {1.resname}{1.id[1]} < Fragment {0} > {2.parent.id} {2.resname}{2.id[1]}".format(
                    i_pp, pp[0], pp[-1]
                )
            )
        # raise Exception('Calculation cannot proceed')

    return (s, n_chains, n_res)
