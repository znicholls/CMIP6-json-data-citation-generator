import re


def deep_substitute(input_val, substitutions):
    """Substitute strings in the input recursively

    In the input, strings contained between carets e.g. '<name>', will be replaced
    with the corresponding value in ``substitutions``. Before looking for a
    replacement, the carets are removed. For example, '<name>' will be replaced with
    ``substitutions["name"]``.

    Note that keys in any input value which is a dictionary will not be replaced, see
    the examples.

    Parameters
    ----------
    input_val: str, float, int, list, dict, nested structures of the above
        The object in which the substitutions should be made

    substitutions: dict
        The substitutions to make

    Returns
    -------
    type(input_val):
        The input_val with all substitutions made

    Raises
    ------
    KeyError
        If no substitution can be found

    Examples
    --------
    >>> deep_substitute("<source_id>", {"source_id": "UoM"})
    'UoM'

    >>> deep_substitute(["<source_id>", "other string"], {"source_id": "UoM"})
    ['UoM', 'other string']

    >>> deep_substitute([["<source_id>", "other string"], "<activity_id>"], {"source_id": "UoM", "activity_id": "21st Century runs"})
    [['UoM', 'other string'], '21st Century runs']

    >>> deep_substitute([{"other string": "<source_id>"}, "<activity_id>"], {"source_id": "UoM", "activity_id": "21st Century runs"})
    [{'other string': 'UoM'}, '21st Century runs']

    >>> # keys in input dictionaries are not substituted
    >>> deep_substitute({"<source_id>": "<source_id>"}, {"source_id": "UoM"})
    {'<source_id>': 'UoM'}

    >>> # missing substitutions will raise ``KeyError``
    >>> deep_substitute("<source_id>", {"activity_id": "21st Century runs"})
    KeyError: "No substitution provided for ['<source_id>']"
    """
    if isinstance(input_val, list):
        for i, val in enumerate(input_val):
            input_val[i] = deep_substitute(val, substitutions)
    elif isinstance(input_val, dict):
        for key, value in input_val.items():
            input_val[key] = deep_substitute(value, substitutions)
    else:
        for old_str, new_str in substitutions.items():
            replacement = "<{}>".format(old_str)
            try:
                input_val = input_val.replace(replacement, new_str)
            except AttributeError:
                return input_val

        if ("<" in input_val) or (">" in input_val):
            unsubstituted_strings = re.findall("<[^<]*>", input_val)
            error_msg = "No substitution provided for {}".format(unsubstituted_strings)
            raise KeyError(error_msg)

    return input_val

