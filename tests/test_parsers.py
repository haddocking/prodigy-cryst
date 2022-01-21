from . import DATA_FOLDER
from pathlib import Path
from Bio.PDB.Structure import Structure
from prodigy_cryst.lib.parsers import parse_structure


def test_parse_structure():
    """Test the structure parser."""

    pdb_path = Path(DATA_FOLDER, "1ppe.pdb")

    s, n_chains, n_res = parse_structure(pdb_path)

    assert isinstance(s, Structure)
    assert n_chains == 2
    assert n_res == 252
