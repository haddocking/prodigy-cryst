#!/usr/bin/env python
#
# This code is part of the interface classifier tool distribution
# and governed by its license.  Please see the LICENSE file that should
# have been included as part of this package.
#

"""
Biological/crystallographic interface classifier based on Intermolecular Contacts (ICs).
"""

from __future__ import print_function, division

__author__ = ["Katarina Elez", "Anna Vangone", "Joao Rodrigues", "Brian Jimenez"]

import os
import sys

try:
    from Bio.PDB import NeighborSearch
except ImportError as e:
    print('[!] The interface classifier tool requires Biopython', file=sys.stderr)
    raise ImportError(e)

from lib.freesasa import execute_freesasa
from lib.utils import _check_path
from lib.parsers import parse_structure
from lib import aa_properties


def calculate_ic(structure, d_cutoff=5.0, selection=None):
    """
    Calculates intermolecular contacts in a parsed structure object.
    """
    atom_list = list(structure.get_atoms())
    ns = NeighborSearch(atom_list)
    all_list = ns.search_all(radius=d_cutoff, level='R')

    if selection:
        _sd = selection_dict
        _chain = lambda x: x.parent.id
        ic_list = [c for c in all_list if (_chain(c[0]) in _sd and _chain(c[1]) in _sd)
                    and (_sd[_chain(c[0])] != _sd[_chain(c[1])]) ]
    else:
        ic_list = [c for c in all_list if c[0].parent.id != c[1].parent.id]

    if not ic_list:
        raise ValueError('No contacts found for selection')

    return ic_list


def analyse_contacts(contact_list):
    """
    Enumerates and classifies contacts based on the chemical characteristics
    of the participating amino acids.
    """

    bins = {
        'AA': 0, 'PP': 0, 'CC': 0, 'AP': 0, 'CP': 0, 'AC': 0,
        'ALA': 0, 'CYS': 0, 'GLU': 0, 'ASP': 0, 'GLY': 0,
        'PHE': 0, 'ILE': 0, 'HIS': 0, 'LYS': 0, 'MET': 0,
        'LEU': 0, 'ASN': 0, 'GLN': 0, 'PRO': 0, 'SER': 0,
        'ARG': 0, 'THR': 0, 'TRP': 0, 'VAL': 0, 'TYR': 0,
        }

    _data = aa_properties.aa_character_ic
    for (res_i, res_j) in contact_list:
        contact_type = (_data.get(res_i.resname), _data.get(res_j.resname))
        contact_type = ''.join(sorted(contact_type))
        bins[contact_type] += 1
        bins[res_i.resname] += 1
        bins[res_j.resname] += 1

    return bins


if __name__ == "__main__":

    try:
        import argparse
        from argparse import RawTextHelpFormatter
    except ImportError as e:
        print('[!] The interface classifier tool requires Python 2.7+', file=sys.stderr)
        raise ImportError(e)

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    ap.add_argument('structf', help='Structure to analyse in PDB or mmCIF format')
    ap.add_argument('--contact_list', action='store_true', help='Output a list of contacts')
    ap.add_argument('-q', '--quiet', action='store_true', help='Outputs only the predicted interface class')

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
    sel_opt = ap.add_argument_group('Selection Options', description=_co_help)
    sel_opt.add_argument('--selection', nargs='+', metavar=('A B', 'A,B C'))

    cmd = ap.parse_args()

    if cmd.quiet:
        _stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    struct_path = _check_path(cmd.structf)

    # Parse structure
    structure, n_chains, n_res = parse_structure(struct_path)
    print('[+] Parsed structure file {0} ({1} chains, {2} residues)'.format(structure.id, n_chains, n_res))

    # Make selection dict from user option or PDB chains
    if cmd.selection:
        selection_dict = {}
        for igroup, group in enumerate(cmd.selection):
            chains = group.split(',')
            for chain in chains:
                if chain in selection_dict:
                    errmsg = 'Selections must be disjoint sets: {0} is repeated'.format(chain)
                    raise ValueError(errmsg)
                selection_dict[chain] = igroup
    else:
        selection_dict = dict([(c.id, nc) for nc, c in enumerate(structure.get_chains())])

    # Contacts
    ic_network = calculate_ic(structure, selection=selection_dict)
    print('[+] No. of intermolecular contacts: {0}'.format(len(ic_network)))

    bins = analyse_contacts(ic_network)

    # SASA
    _, cmplx_sasa = execute_freesasa(structure, selection=selection_dict)
        
    # Print out features
    print('[+] No. of charged-charged contacts: {0}'.format(bins['CC']))
    print('[+] No. of charged-polar contacts: {0}'.format(bins['CP']))
    print('[+] No. of charged-apolar contacts: {0}'.format(bins['AC']))
    print('[+] No. of polar-polar contacts: {0}'.format(bins['PP']))
    print('[+] No. of apolar-polar contacts: {0}'.format(bins['AP']))
    print('[+] No. of apolar-apolar contacts: {0}'.format(bins['AA']))
    for aa in ['ALA', 'CYS', 'GLU', 'ASP', 'GLY', 'PHE', 'ILE', 'HIS', 'LYS', 'MET', 'LEU', 'ASN', 'GLN', 'PRO', 'SER', 'ARG', 'THR', 'TRP', 'VAL', 'TYR']:
        print('[+] '+aa+': '+str(bins[aa]))

    list1, list2 = zip(*ic_network)
    max_contacts = len(set(list1))*len(set(list2))
    print('[+] Link density: {0:3.4f}'.format(len(ic_network)/max_contacts))    

    # Print out interaction network
    if cmd.contact_list:
        fname = struct_path[:-4] + '.ic'
        with open(fname, 'w') as ic_handle:
            for pair in ic_network:
                _fmt_str = "{0.parent.id}\t{0.resname}\t{0.id[1]}\t{1.parent.id}\t{1.resname}\t{1.id[1]}".format(*pair)
                print(_fmt_str, file=ic_handle)
   
    # Predict and print out interface type
    features = [str(bins[x]) for x in ['CP', 'AC', 'AP', 'AA', 
        'ALA', 'CYS', 'GLU', 'ASP', 'GLY', 'PHE', 'ILE', 'HIS', 'MET', 'LEU', 'GLN', 'PRO', 'SER', 'ARG', 'THR', 'VAL', 'TYR']]
    features.append(str(len(ic_network)/max_contacts))
    base_path = os.path.dirname(os.path.realpath(__file__))
    prediction = os.popen(os.path.join(base_path, 'classify.py') + ' ' + ' '.join(features)).read()
    print('[+] Class: '+prediction)

    if cmd.quiet:
        sys.stdout = _stdout
        print('[+] Class: '+prediction)
