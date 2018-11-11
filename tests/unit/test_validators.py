import re


import pytest
from marshmallow import ValidationError


from cmip6_data_citation_generator.validators import CitationSchema


def test_load_template_yaml(valid_yaml):
    CitationSchema(strict=True).load(valid_yaml)


@pytest.mark.parametrize("field_to_delete", ["fundingReferences", "relatedIdentifiers"])
def test_load_template_yaml_missing_optional_field(valid_yaml, field_to_delete):
    del valid_yaml[field_to_delete]
    CitationSchema(strict=True).load(valid_yaml)


@pytest.mark.parametrize(
    "field_to_delete", ["contributors", "creators", "subjects", "titles"]
)
def test_load_template_yaml_missing_compulsory_field(valid_yaml, field_to_delete):
    del valid_yaml[field_to_delete]
    error_msg = (
        "^.*" + "{}".format(field_to_delete) + ".*Missing data for required field.*$"
    )
    with pytest.raises(ValidationError, match=error_msg):
        CitationSchema(strict=True).load(valid_yaml)


def test_load_template_yaml_missing_dependent_field(valid_yaml):
    tlevel = "subjects"
    del valid_yaml[tlevel][0]["schemeURI"]
    error_msg = re.escape(
        "The fields {} in {} are co-dependent, if you supply one of them, you must "
        "supply all of them".format(["schemeURI", "subjectScheme"], tlevel)
    )
    with pytest.raises(ValidationError, match=error_msg):
        CitationSchema(strict=True).load(valid_yaml)
