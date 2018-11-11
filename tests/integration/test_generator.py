from conftest import TEST_VALID_INPUT_YAML


from cmip6_data_citation_generator import load_template_yaml


def test_load_template_yaml():
    validated_schema = load_template_yaml(TEST_VALID_INPUT_YAML)

    assert isinstance(validated_schema, dict)
    assert (
        validated_schema["contributors"][1]["contributorName"]
        == "Institut Pierre Simon Laplace (IPSL)"
    )
