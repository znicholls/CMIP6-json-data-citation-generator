from os import remove
from os.path import isfile
import re


import pytest
from marshmallow import ValidationError


from conftest import TEST_VALID_INPUT_YAML
from cmip6_data_citation_generator.io_dcg import (
    load_and_validate_yaml,
    validate_and_return_raw_dict,
    write_json,
    _add_compulsory_subject,
)


def test_load_and_validate_yaml():
    validated_schema = load_and_validate_yaml(TEST_VALID_INPUT_YAML)

    assert isinstance(validated_schema, dict)
    assert (
        validated_schema["contributors"][1]["contributorName"]
        == "Institut Pierre Simon Laplace (IPSL)"
    )


@pytest.mark.parametrize("field_to_delete", ["fundingReferences", "relatedIdentifiers"])
def test_validate_and_return_raw_dict_missing_optional_field(
    valid_yaml_dict, field_to_delete
):
    del valid_yaml_dict[field_to_delete]
    validate_and_return_raw_dict(valid_yaml_dict)


@pytest.mark.parametrize(
    # "field_to_delete", ["contributors", "creators", "subjects", "titles"]
    "field_to_delete",
    ["subjects"],
)
def test_validate_and_return_raw_dict_missing_compulsory_field(
    valid_yaml_dict, field_to_delete
):
    del valid_yaml_dict[field_to_delete]
    error_msg = (
        "^.*" + "{}".format(field_to_delete) + ".*Missing data for required field.*$"
    )
    with pytest.raises(ValidationError, match=error_msg):
        validate_and_return_raw_dict(valid_yaml_dict)


def test_validate_and_return_raw_dict_missing_subject_field(valid_yaml_dict):
    del valid_yaml_dict["subjects"][0]
    error_msg = re.escape(
        "{'subjects': [\"^The first element under subjects should be autofilled by "
        "the generator and hence be equal to {'subject': '<subject>', "
        "'subjectScheme': 'DRS', 'schemeURI': "
        "'http://github.com/WCRP-CMIP/CMIP6_CVs'}\"]}"
    )
    with pytest.raises(ValidationError, match=error_msg):
        validate_and_return_raw_dict(valid_yaml_dict)


def test_validate_and_return_raw_dict_missing_dependent_field(valid_yaml_dict):
    tlevel = "subjects"
    del valid_yaml_dict[tlevel][0]["schemeURI"]
    error_msg = re.escape(
        "The fields {} in {} are co-dependent, if you supply one of them, you must "
        "supply all of them".format(["schemeURI", "subjectScheme"], tlevel)
    )
    with pytest.raises(ValidationError, match=error_msg):
        validate_and_return_raw_dict(valid_yaml_dict)


def test_validate_and_return_raw_dict_extra_field(valid_yaml_dict):
    valid_yaml_dict["junk"] = [{"extra": "field"}]
    error_msg = re.escape("{'junk': ['Unknown field.']}")
    with pytest.raises(ValidationError, match=error_msg):
        validate_and_return_raw_dict(valid_yaml_dict)


def test_add_compulsory_subject(valid_yaml_dict):
    compulsory_subject = {
        "subject": "<subject>",
        "subjectScheme": "DRS",
        "schemeURI": "http://github.com/WCRP-CMIP/CMIP6_CVs",
    }

    result = _add_compulsory_subject({})
    expected = {"subjects": [compulsory_subject]}
    assert result == expected

    result_again = _add_compulsory_subject(result)
    expected_again = {"subjects": [compulsory_subject, compulsory_subject]}
    assert result_again == expected_again


def test_write_json():
    tout_file = "tjson.json"
    tdict = {"string": 34, "key": ["hi", "bye"]}

    write_json(tdict, tout_file)

    assert isfile(tout_file)

    with open(tout_file, "r") as f:
        result = f.read()

    expected = (
        '{\n    "key": [\n        "hi",\n        "bye"\n    ],\n    "string": 34\n}'
    )

    assert result == expected
    remove(tout_file)
