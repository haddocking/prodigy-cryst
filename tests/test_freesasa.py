from prodigy_cryst.lib.freesasa import (
    freesasa_version,
    execute_freesasa,
    # parse_freesasa_output,
)
import pytest
from tests import DATA_FOLDER
from pathlib import Path
from prodigy_cryst.lib.parsers import parse_structure


@pytest.fixture
def parsed_structure():
    pdb_path = Path(DATA_FOLDER, "1ppe.pdb")
    s, _, _ = parse_structure(pdb_path)
    return s


@pytest.mark.skip(reason="Function not used")
def test_freesasa_version():
    """Test the check of freesasa version."""
    major, minor = freesasa_version()

    assert type(major) == int
    assert type(minor) == int


@pytest.mark.skip(reason="Function not used")
def test_execute_freesasa(parsed_structure):
    """Test if freesasa can calculate asa/rsa."""
    asa, rsa = execute_freesasa(parsed_structure)

    assert asa[("E", "ILE", 16, "O")] == pytest.approx(1.43)
    assert rsa[("E", "GLY", 18)] == pytest.approx(0.55, 0.1)


# embedded in execute_freesasa
# def test_parse_freesasa_output():
#     pass
