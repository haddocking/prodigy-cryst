from pathlib import Path

from Bio.PDB.Structure import Structure

from prodigy_cryst.lib.parsers import parse_structure

from . import DATA_FOLDER


def test_parse_structure():
    """Test the structure parser."""

    pdb_path = Path(DATA_FOLDER, "complex.pdb")

    s, n_chains, n_res = parse_structure(pdb_path)

    assert isinstance(s, Structure)
    assert n_chains == 2
    assert n_res == 252

    pdb_w_gaps_path = Path(DATA_FOLDER, "complex_w_gaps.pdb")

    s_gaps, n_chains_gaps, n_res_gaps = parse_structure(pdb_w_gaps_path)

    assert isinstance(s_gaps, Structure)
    assert n_chains_gaps == 2
    assert n_res_gaps == 247
