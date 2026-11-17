from pathlib import Path

import pytest
from Bio.PDB.Structure import Structure

from prodigy_cryst.modules.parsers import parse_structure

from . import DATA_FOLDER


def test_parse_structure():
    """Test the structure parser."""

    pdb_path = Path(DATA_FOLDER, "complex.pdb")

    s, n_chains, n_res = parse_structure(pdb_path)

    assert isinstance(s, Structure)
    assert n_chains == 2
    assert n_res == 252

    with pytest.raises(Exception):
        parse_structure("nothing.pdb")

    pdb_w_gaps_path = Path(DATA_FOLDER, "ens_w_gaps.pdb")
    s_gaps, n_chains_gaps, n_res_gaps = parse_structure(pdb_w_gaps_path)

    assert isinstance(s_gaps, Structure)
    assert n_chains_gaps == 2
    assert n_res_gaps == 247


def test_parse_structure_forcefield_resnames(tmp_path):
    """Force-field names of standard residues are read as the standard residue."""
    pdb_path = Path(tmp_path, "complex_hsd.pdb")
    pdb = Path(DATA_FOLDER, "complex.pdb").read_text()
    pdb_path.write_text(pdb.replace(" HIS ", " HSD "))

    s, _, _ = parse_structure(pdb_path)

    resnames = [r.resname for r in s.get_residues()]
    assert "HSD" not in resnames
    assert "HIS" in resnames
