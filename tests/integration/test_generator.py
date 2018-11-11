from conftest import TEST_VALID_INPUT_YAML


def test_load_template_yaml():
    validated_schema = load_template_yaml(TEST_VALID_INPUT_YAML)
