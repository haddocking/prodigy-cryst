#!/usr/bin/env python
#
# This code is part of the interface classifier tool distribution
# and governed by its license.  Please see the LICENSE file that should
# have been included as part of this package.
#

"""
Biological/crystallographic interface classifier based on Intermolecular Contacts (ICs).
"""

from __future__ import division, print_function

__author__ = ["Katarina Elez", "Anna Vangone", "Joao Rodrigues", "Brian Jimenez"]

import logging
import pickle

# import os
import sys
import warnings
from pathlib import Path

try:
    from Bio.PDB import NeighborSearch
except ImportError as e:
    logging.error("[!] The interface classifier tool requires Biopython")
    raise ImportError(e)

from prodigy_cryst.lib import aa_properties
from prodigy_cryst.lib.parsers import parse_structure

# from prodigy_cryst.lib.freesasa import execute_freesasa
from prodigy_cryst.lib.utils import _check_path


def calculate_ic(structure, d_cutoff=5.0, selection=None):
    """
    Calculates intermolecular contacts in a parsed structure object.
    """
    atom_list = list(structure.get_atoms())
    ns = NeighborSearch(atom_list)
    all_list = ns.search_all(radius=d_cutoff, level="R")

    if selection:
        _sd = selection

        def _chain(x):
            return x.parent.id

        ic_list = [
            c
            for c in all_list
            if (_chain(c[0]) in _sd and _chain(c[1]) in _sd)
            and (_sd[_chain(c[0])] != _sd[_chain(c[1])])
        ]
    else:
        ic_list = [c for c in all_list if c[0].parent.id != c[1].parent.id]

    if not ic_list:
        raise ValueError("No contacts found for selection")

    return ic_list


def analyse_contacts(contact_list):
    """
    Enumerates and classifies contacts based on the chemical characteristics
    of the participating amino acids.
    """

    bins = {
        "AA": 0,
        "PP": 0,
        "CC": 0,
        "AP": 0,
        "CP": 0,
        "AC": 0,
        "ALA": 0,
        "CYS": 0,
        "GLU": 0,
        "ASP": 0,
        "GLY": 0,
        "PHE": 0,
        "ILE": 0,
        "HIS": 0,
        "LYS": 0,
        "MET": 0,
        "LEU": 0,
        "ASN": 0,
        "GLN": 0,
        "PRO": 0,
        "SER": 0,
        "ARG": 0,
        "THR": 0,
        "TRP": 0,
        "VAL": 0,
        "TYR": 0,
    }

    _data = aa_properties.aa_character_ic
    for (res_i, res_j) in contact_list:
        contact_type = (_data.get(res_i.resname), _data.get(res_j.resname))
        contact_type = "".join(sorted(contact_type))
        bins[contact_type] += 1
        bins[res_i.resname] += 1
        bins[res_j.resname] += 1

    return bins


class ProdigyCrystal:
    # init parameters
    def __init__(self, struct_obj, selection=None):
        if selection is None:
            self.selection = [chain.id for chain in struct_obj.get_chains()]
        else:
            self.selection = selection
        self.structure = struct_obj
        self.ic_network = {}
        self.bins = {}
        self.nis_a = 0
        self.nis_c = 0
        self.ba_val = 0
        self.kd_val = 0

    def predict(self, temp=None, distance_cutoff=5.5, acc_threshold=0.05):
        # Make selection dict from user option or PDB chains
        if self.selection:
            selection_dict = {}
            for igroup, group in enumerate(self.selection):
                chains = group.split(",")
                for chain in chains:
                    if chain in selection_dict:
                        errmsg = (
                            "Selections must be disjoint sets: {0} is repeated".format(
                                chain
                            )
                        )
                        raise ValueError(errmsg)
                    selection_dict[chain] = igroup
        else:
            selection_dict = dict(
                [(c.id, nc) for nc, c in enumerate(self.structure.get_chains())]
            )

        # Contacts
        self.ic_network = calculate_ic(self.structure, selection=selection_dict)

        self.bins = analyse_contacts(self.ic_network)

        # =====
        # This is not used!
        # SASA
        # _, cmplx_sasa = execute_freesasa(self.structure, selection=selection_dict)
        # =====

        # Link density
        list1, list2 = zip(*(self.ic_network))
        max_contacts = len(set(list1)) * len(set(list2))
        self.link_density = len(self.ic_network) / max_contacts

        # Predict and print out interface type
        features = [
            str(self.bins[x])
            for x in [
                "CP",
                "AC",
                "AP",
                "AA",
                "ALA",
                "CYS",
                "GLU",
                "ASP",
                "GLY",
                "PHE",
                "ILE",
                "HIS",
                "MET",
                "LEU",
                "GLN",
                "PRO",
                "SER",
                "ARG",
                "THR",
                "VAL",
                "TYR",
            ]
        ]
        features.append(str(len(self.ic_network) / max_contacts))
        # Q: Why is this calling classify?
        # base_path = os.path.dirname(os.path.realpath(__file__))
        # prediction = os.popen(
        #     os.path.join(base_path, "prodigy_cryst", "classify.py")
        #     + " "
        #     + " ".join(features)
        # ).read()
        model_f = Path(
            Path(__file__).resolve().parent.parent, "prodigy_cryst/data/classifier.sav"
        )
        # Calling this will raise some warning about modules that will be deprecated
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with open(model_f, "rb") as fh:
                model = pickle.load(fh)
            proba = list(model.predict_proba([features])[0])
            prediction = ["BIO", "XTAL"][proba.index(max(proba))], proba[0], proba[1]
        self.predicted_class = prediction

    def as_dict(self):
        return_dict = {
            "structure": self.structure.id,
            "selection": self.selection,
            "ICs": len(self.ic_network),
            "link_density": self.link_density,
            "predicted_class": self.predicted_class,
        }
        return_dict.update(self.bins)
        return return_dict

    def print_prediction(self, outfile="", quiet=False):
        if outfile:
            handle = open(outfile, "w")
        else:
            handle = sys.stdout

        if quiet:
            handle.write(
                "[+] {0}\t{1}\n".format(self.structure.id, self.predicted_class)
            )
        else:
            handle.write("[+] Selection: {0}\n".format(", ".join(self.selection)))
            handle.write(
                "[+] No. of intermolecular contacts: {0}\n".format(len(self.ic_network))
            )
            handle.write(
                "[+] No. of charged-charged contacts: {0}\n".format(self.bins["CC"])
            )
            handle.write(
                "[+] No. of charged-polar contacts: {0}\n".format(self.bins["CP"])
            )
            handle.write(
                "[+] No. of charged-apolar contacts: {0}\n".format(self.bins["AC"])
            )
            handle.write(
                "[+] No. of polar-polar contacts: {0}\n".format(self.bins["PP"])
            )
            handle.write(
                "[+] No. of apolar-polar contacts: {0}\n".format(self.bins["AP"])
            )
            handle.write(
                "[+] No. of apolar-apolar contacts: {0}\n".format(self.bins["AA"])
            )
            handle.write("[+] Link density: {0:3.2f}\n".format(self.link_density))
            # handle.write("[+] Class: {}\n".format(self.predicted_class))
            values = self.predicted_class
            handle.write(f"[+] Class: {values[0]} {values[1]} {values[2]}\n")

        if handle is not sys.stdout:
            handle.close()

    def print_contacts(self, outfile=""):
        if outfile:
            handle = open(outfile, "w")
        else:
            handle = sys.stdout

        for res1, res2 in self.ic_network:
            _fmt_str = (
                "{0.resname:>5s} {0.id[1]:5} {0.parent.id:>3s} {1.resname:>5s}"
                " {1.id[1]:5} {1.parent.id:>3s}\n"
            )
            if res1.parent.id not in self.selection[0]:
                res1, res2 = res2, res1
            handle.write(_fmt_str.format(res1, res2))

        if handle is not sys.stdout:
            handle.close()


def main():

    try:
        import argparse
        from argparse import RawTextHelpFormatter
    except ImportError as e:
        print("[!] The interface classifier tool requires Python 2.7+", file=sys.stderr)
        raise ImportError(e)

    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawTextHelpFormatter
    )
    ap.add_argument("structf", help="Structure to analyse in PDB or mmCIF format")
    ap.add_argument(
        "--contact_list", action="store_true", help="Output a list of contacts"
    )
    ap.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Outputs only the predicted interface class",
    )

    _co_help = """
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
    """
    sel_opt = ap.add_argument_group("Selection Options", description=_co_help)
    sel_opt.add_argument("--selection", nargs="+", metavar=("A B", "A,B C"))

    cmd = ap.parse_args()

    # setup logging
    log_level = logging.ERROR if cmd.quiet else logging.INFO
    logging.basicConfig(level=log_level, format="%(message)s")
    # logger = logging.getLogger("Prodigy")

    struct_path = _check_path(cmd.structf)

    # Parse structure
    structure, n_chains, n_res = parse_structure(struct_path)
    prodigy = ProdigyCrystal(structure, cmd.selection)
    prodigy.predict()
    prodigy.print_prediction(quiet=cmd.quiet)

    # Print out interaction network
    if cmd.contact_list:
        fname = struct_path[:-4] + ".ic"
        prodigy.print_contacts(fname)
