import re


import pytest


from cmip6_data_citation_generator.utils import deep_substitute


@pytest.mark.parametrize(
    "input_value,expected",
    [
        ("<source_id>", "rsouce_id"),
        ("nor", "nor"),
        (2, 2),
        (["<source_id>", "<source_id>"], ["rsouce_id", "rsouce_id"]),
        (["nor", "<activity_id>"], ["nor", "ractivity_id"]),
        (["nor", "nor"], ["nor", "nor"]),
        (["nor", "<source_id>", 3], ["nor", "rsouce_id", 3]),
        ([{"nor": "<source_id>", "key": 3}], [{"nor": "rsouce_id", "key": 3}]),
        (
            {
                "<activity_id>": "nor",
                "other_key": "<source_id>",
                "final_key": [{"bottom_key": "<institution_id>"}],
            },
            {
                "<activity_id>": "nor",
                "other_key": "rsouce_id",
                "final_key": [{"bottom_key": "rinstitution_id"}],
            },
        ),
    ],
)
def test_deep_substitute(input_value, expected):
    subst_dict = {
        "source_id": "rsouce_id",
        "activity_id": "ractivity_id",
        "institution_id": "rinstitution_id",
    }

    result = deep_substitute(input_value, subst_dict)
    assert result == expected


def test_deep_substitute_error_no_substitution_single_error():
    subst_dict = {"source_id": "rsouce_id"}
    error_msg = re.escape("No substitution provided for ['<activity_id>']")
    with pytest.raises(KeyError, match=error_msg):
        deep_substitute("<activity_id>", subst_dict)


def test_deep_substitute_error_no_substitution_multiple_error():
    subst_dict = {"source_id": "rsouce_id"}
    error_msg = re.escape(
        "No substitution provided for ['<activity_id>', '<institution_id>']"
    )
    with pytest.raises(KeyError, match=error_msg):
        deep_substitute("<activity_id> from <institution_id>", subst_dict)
