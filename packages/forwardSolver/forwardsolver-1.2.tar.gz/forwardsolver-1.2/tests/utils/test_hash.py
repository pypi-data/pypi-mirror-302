from forwardSolver.scripts.utils.hash import hash_dictionary


def test_hash_function():

    # Permutations shouldn't matter
    assert hash_dictionary({"b": 2, "a": 1}) == hash_dictionary({"a": 1, "b": 2})

    # Numbers should all be treated as floats
    assert hash_dictionary({"b": 2.0, "a": 1}) == hash_dictionary({"b": 2, "a": 1.0})

    # None values ignored
    assert hash_dictionary({"b": None, "a": 1}) == hash_dictionary({"a": 1.0})

    # Git SHA should be included
    assert "no_repo" not in hash_dictionary({"a": 1, "b": 2})

    # Nesting should be included
    assert hash_dictionary({"a": {"b": 1, "c": 2}, "d": 3}) != hash_dictionary(
        {"a": {"b": 1, "c": 3}, "d": 3}
    )
