#!/usr/bin/env python
#
# This code is part of the interface classifier tool distribution
# and governed by its license.  Please see the LICENSE file that should
# have been included as part of this package.
#

"""
Generic properties of amino acids required for the interface classification methods.
"""

__author__ = ["Anna Vangone", "Joao Rodrigues"]

aa_character_ic = {
    'ALA': 'A',
    'CYS': 'A', # ?
    'GLU': 'C',
    'ASP': 'C',
    'GLY': 'A',
    'PHE': 'A',
    'ILE': 'A',
    'HIS': 'C',
    'LYS': 'C',
    'MET': 'A',
    'LEU': 'A',
    'ASN': 'P',
    'GLN': 'P',
    'PRO': 'A',
    'SER': 'P',
    'ARG': 'C',
    'THR': 'P',
    'TRP': 'A',
    'VAL': 'A',
    'TYR': 'A',
}

aa_character_protorp = {
    'ALA': 'A',
    'CYS': 'P',
    'GLU': 'C',
    'ASP': 'C',
    'GLY': 'A',
    'PHE': 'A',
    'ILE': 'A',
    'HIS': 'P',
    'LYS': 'C',
    'MET': 'A',
    'LEU': 'A',
    'ASN': 'P',
    'GLN': 'P',
    'PRO': 'A',
    'SER': 'P',
    'ARG': 'C',
    'THR': 'P',
    'TRP': 'P',
    'VAL': 'A',
    'TYR': 'P',
}
