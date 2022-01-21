from prodigy_cryst.lib.aa_properties import (
    rel_asa,
    aa_character_ic,
    aa_character_protorp,
)
import pytest


def test_properties():
    """Test if the properties are defined."""
    assert rel_asa["total"]["ALA"] == pytest.approx(107.95)
    assert rel_asa["bb"]["ALA"] == pytest.approx(38.54)
    assert rel_asa["sc"]["ALA"] == pytest.approx(69.41)
    assert aa_character_protorp["GLU"] == "C"
    assert aa_character_ic["ARG"] == "C"
