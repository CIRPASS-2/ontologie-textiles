"""The approved Phase 2B release remains reproducible offline from Git."""
import pytest
from scripts.reconstruct_phase2b import reconstruct


def test_reconstruct_phase2b_into_isolated_directory(tmp_path):
    destination = tmp_path / 'phase2b'
    assert reconstruct(destination) == (815, 814, 20)
    with pytest.raises(FileExistsError):
        reconstruct(destination)
