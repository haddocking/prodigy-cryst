from tempfile import NamedTemporaryFile

from prodigy_cryst.lib.utils import _check_path


def test__check_path():
    """Test the check path function."""
    temp_f = NamedTemporaryFile(delete=False, suffix=".out")
    expected_output = _check_path(temp_f.name)

    assert ".out" in expected_output
