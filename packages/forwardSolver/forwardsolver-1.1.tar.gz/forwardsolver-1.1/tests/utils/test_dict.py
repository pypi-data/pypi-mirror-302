import pytest

from forwardSolver.scripts.utils.dict import check_all_keys_none


@pytest.mark.parametrize(
    "test_dict, test_allow_empty,result",
    [
        ({}, True, True),  # empty dict return true
        ({}, False, False),  # empty dict return false if empty dict not allowed
        ({"a": None}, False, True),  # one None value return True
        ({"a": {"a": None}}, False, True),  # nested None value return True
        ({"a": 1, "b": None}, False, False),  # non-None value return False
        ({"a": None, "b": 2}, False, False),  # non-None value return False
        (
            {"a": {"a": 1, "b": None}},
            False,
            False,
        ),  # nested non-None value return False
        (
            {"a": {"a": None, "b": 1}},
            False,
            False,
        ),  # nested non-None value return False
    ],
)
def test_check_all_keys_none(test_dict, test_allow_empty, result):
    """
    Checks to see if the `check_all_keys_none` function works as expected.
    Function should return `True` if all keys in the dictionary have a value of `None`.
    If `test_allow_empty` is set to `True` then will treat and empty dictionary result as containing `None`
    """
    assert (
        check_all_keys_none(test_dict, allow_empty_dictionaries=test_allow_empty)
        == result
    )
