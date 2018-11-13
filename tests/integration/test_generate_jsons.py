from os import remove
from os.path import isfile
import re


import pytest


from conftest import (
    TEST_DATA_CMIP6_OUTPUT_STYLE,
    TEST_VALID_INPUT_YAML,
)
from cmip6_data_citation_generator import generate_jsons


def test_get_unique_subjects_in_dir_cmip6output_style():
    generate_jsons(TEST_DATA_CMIP6_OUTPUT_STYLE, TEST_VALID_INPUT_YAML, "CMIP6output", ".", regexp=".*")

    expected_file = "./CMIP6.DCPP.CNRM-CERFACS.CNRM-CM6-1.json"

    assert isfile(expected_file)
    remove(expected_file)
