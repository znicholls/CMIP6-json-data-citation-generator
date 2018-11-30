from os.path import join, dirname, abspath
from copy import deepcopy


import pytest
import yaml


from cmip6_data_citation_generator.io_dcg import _add_compulsory_subject


TEST_DATA_ROOT_DIR = join(dirname(abspath(__file__)), "test_data")

TEST_DATA_CMIP6_INPUT4MIPS_STYLE = join(TEST_DATA_ROOT_DIR, "input4MIPs_like")
TEST_DATA_CMIP6_OUTPUT_STYLE = join(TEST_DATA_ROOT_DIR, "CMIP6output_like")
TEST_DATA_FLATTISH_STYLE = join(TEST_DATA_ROOT_DIR, "flattish_files")

TEST_VALID_INPUT_YAML = join(TEST_DATA_ROOT_DIR, "valid_input.yaml")
TEST_SPECIAL_CHAR_YAML = join(TEST_DATA_ROOT_DIR, "special_char_input.yaml")
TEST_VALID_OUTPUT_JSON = join(TEST_DATA_ROOT_DIR, "valid_output.json")


@pytest.fixture(scope="session")
def base_valid_yaml_dict():
    with open(TEST_VALID_INPUT_YAML, "r") as stream:
        yield yaml.safe_load(stream)


@pytest.fixture(scope="function")
def valid_yaml_dict(base_valid_yaml_dict):
    yield _add_compulsory_subject(deepcopy(base_valid_yaml_dict))
