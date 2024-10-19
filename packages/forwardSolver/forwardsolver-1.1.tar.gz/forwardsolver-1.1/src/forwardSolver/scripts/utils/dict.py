def nested_set(dic, keys, value):
    """
    Helper function to set a value in a dict

    e.g.
    >>> nested_set(dic, ['a', 'b'], 10)
    is idendtical to
    >>> dic['a']['b'] = 10
    """
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def nested_get(dic, keys):
    """
    Helper function to get a value in a dict

    i.e.
    >>> nested_get(dic, ['a', 'b']) == dic['a']['b'] = 10
    True
    """
    for key in keys:
        dic = dic[key]
    return dic


def set_dict_val(dic, key_string, val):
    """
    Easy way to set value in a nested dictionary using forward-slashes.

    e.g.
    >>> set_dict_val(dic, 'a/b', 10)
    is idendtical to
    >>> dic['a']['b'] = 10
    """
    nested_keys = key_string.split("/")
    nested_set(dic, nested_keys, val)


def get_dict_val(dic, key_string):
    """
    Easy way to get value in a nested dictionary using forward-slashes.

    e.g.
    >>> get_dict_val(dic, 'a/b', 10)
    is idendtical to
    >>> dic['a']['b'] = 10
    """
    nested_keys = key_string.split("/")
    return nested_get(dic, nested_keys)


def check_all_keys_none(dictionary: dict, allow_empty_dictionaries=False):
    """
    Checks to see if element in the dictionary is set to `None`
    """

    # Return false if empty dictionary.
    if dictionary == {} and not allow_empty_dictionaries:
        return False

    for k, v in dictionary.items():

        if isinstance(dictionary[k], dict):

            if not check_all_keys_none(
                dictionary[k],
                allow_empty_dictionaries=allow_empty_dictionaries,
            ):
                return False

        elif v is not None:
            return False
    return True
