from os.path import join, dirname, abspath
from copy import deepcopy


import pytest
import yaml


TEST_DATA_ROOT_DIR = join(dirname(abspath(__file__)), "test_data")
TEST_VALID_INPUT_YAML = join(TEST_DATA_ROOT_DIR, "valid_input.yaml")


@pytest.fixture(scope="session")
def base_valid_yaml_dict():
    with open(TEST_VALID_INPUT_YAML, "r") as stream:
        yield yaml.load(stream)


@pytest.fixture(scope="function")
def valid_yaml_dict(base_valid_yaml_dict):
    yield deepcopy(base_valid_yaml_dict)