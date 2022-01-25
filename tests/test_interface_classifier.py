import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from interface_classifier import ProdigyCrystal, analyse_contacts, calculate_ic
from prodigy_cryst.lib.parsers import parse_structure
from tests import DATA_FOLDER


@pytest.fixture
def parsed_structure():
    pdb_path = Path(DATA_FOLDER, "complex.pdb")
    s, _, _ = parse_structure(pdb_path)
    return s


@pytest.fixture
def parsed_structure_w_gaps():
    pdb_path = Path(DATA_FOLDER, "ens_w_gaps.pdb")
    s, _, _ = parse_structure(pdb_path)
    return s


@pytest.fixture
def contact_list():
    pdb_path = Path(DATA_FOLDER, "complex.pdb")
    s, _, _ = parse_structure(pdb_path)
    return [(s[0]["I"][1], s[0]["E"][20])]


@pytest.fixture
def prodigyxtal(parsed_structure):
    return ProdigyCrystal(parsed_structure)


@pytest.fixture
def prodigyxtal_w_gaps(parsed_structure_w_gaps):
    return ProdigyCrystal(parsed_structure_w_gaps)


def test_calculate_ic(parsed_structure):
    """Test the calculation of intramolecular contacts."""
    ic_list = calculate_ic(parsed_structure, d_cutoff=5.0, selection=None)
    assert len(ic_list) == 71

    # this ic_list is randomly sorted, sort it so we can check things
    ic_list.sort()

    assert ic_list[42][0].id == (" ", 194, " ")
    assert ic_list[42][1].id == (" ", 5, " ")
    assert ic_list[42][0].resname == "ASP"
    assert ic_list[42][1].resname == "ARG"


def test_analyse_contacts(contact_list):
    """Test enumeration and classification of contacts."""
    bins = analyse_contacts(contact_list)

    assert len(bins) == 26
    assert bins["AC"] == 1
    assert bins["TYR"] == 1
    assert bins["ARG"] == 1


def test_prodigycrystal_predict(prodigyxtal, prodigyxtal_w_gaps):
    """Test the prediction."""
    prodigyxtal.predict()

    assert prodigyxtal.predicted_class == ("BIO", 0.804, 0.196)

    prodigyxtal_w_gaps.predict()

    assert prodigyxtal_w_gaps.predicted_class == ("BIO", 0.68, 0.32)


def test_prodigycrystal_as_dict(prodigyxtal):
    """Test the dictionary conversion."""
    prodigyxtal.link_density = 0.42
    prodigyxtal.predicted_class = ("BIO", 0.804, 0.196)
    observed_dic = prodigyxtal.as_dict()
    expected_dic = {
        "structure": "complex",
        "selection": ["E", "I"],
        "ICs": 0,
        "link_density": 0.42,
        "predicted_class": ("BIO", 0.804, 0.196),
    }

    assert observed_dic == expected_dic


def test_prodigycrystal_print_prediction(prodigyxtal):
    """Test the printing of the results."""
    prodigyxtal.bins["CC"] = 1
    prodigyxtal.bins["CP"] = 2
    prodigyxtal.bins["AC"] = 3
    prodigyxtal.bins["PP"] = 4
    prodigyxtal.bins["AP"] = 5
    prodigyxtal.bins["AA"] = 6
    prodigyxtal.link_density = 0.42
    prodigyxtal.predicted_class = ("BIO", 0.804, 0.196)

    temp_f = NamedTemporaryFile(delete=False)
    prodigyxtal.print_prediction(outfile=temp_f.name)
    observed_printed_output = "".join(open(temp_f.name).readlines())
    expected_printed_output = (
        "[+] Selection: E, I\n[+] No. of intermolecular contacts: 0\n[+] No. of "
        "charged-charged contacts: 1\n[+] No. of charged-polar contacts: 2\n[+] No. of"
        " charged-apolar contacts: 3\n[+] No. of polar-polar contacts: 4\n[+] No. of"
        " apolar-polar contacts: 5\n[+] No. of apolar-apolar contacts: 6\n[+] Link"
        " density: 0.42\n[+] Class: BIO 0.804 0.196\n"
    )

    assert observed_printed_output == expected_printed_output
    os.unlink(temp_f.name)


def test_prodigycrystal_print_contacts(prodigyxtal, contact_list):
    """Test the printing of the contacts."""
    prodigyxtal.ic_network = contact_list
    temp_f = NamedTemporaryFile(delete=False)
    prodigyxtal.print_contacts(outfile=temp_f.name)

    observed_printed_contacts = "".join(open(temp_f.name).readlines())
    expected_printed_contacts = "  TYR    20   E   ARG     1   I\n"

    assert observed_printed_contacts == expected_printed_contacts

    os.unlink(temp_f.name)
