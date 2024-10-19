import pytest

from forwardSolver.scripts.utils.dict import check_all_keys_none
from forwardSolver.scripts.utils.pixels import Pixels


def test_pixels_initialise_empty():
    # Initialise without args should all be none
    pixels = Pixels(**{})
    assert check_all_keys_none(pixels.as_dict())

    # Initialise with empty dict should all be none
    pixels = Pixels()
    assert check_all_keys_none(pixels.as_dict())


def test_pixels_initialise_key():
    # Should raise TypeError when an extra key is added to dict but not dataclass
    with pytest.raises(TypeError):
        Pixels(**{"donkey123": 123})


def test_pixels_equality():
    # test equality operator and as_dict() function
    pixels1 = Pixels(create_standalone=True, num_pixel_columns=2)
    pixels2 = Pixels(**pixels1.as_dict())
    assert pixels1 == pixels2

    pixels1.create_standalone = False
    assert pixels1 != pixels2
