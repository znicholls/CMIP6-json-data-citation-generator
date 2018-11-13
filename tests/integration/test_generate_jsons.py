from os import remove
from os.path import isfile
import re
import json


import pytest


from conftest import TEST_DATA_CMIP6_OUTPUT_STYLE, TEST_VALID_INPUT_YAML
from cmip6_data_citation_generator import generate_jsons


def test_get_unique_subjects_in_dir_cmip6output_style():
    generate_jsons(
        TEST_DATA_CMIP6_OUTPUT_STYLE,
        TEST_VALID_INPUT_YAML,
        "CMIP6output",
        ".",
        regexp=".*",
    )

    expected_file = "./CMIP6.DCPP.CNRM-CERFACS.CNRM-CM6-1.dcppA-hindcast.json"

    assert isfile(expected_file)

    written = json.loads(open(expected_file).read())

    assert written["contributors"][0]["contributorName"] == "Meinshausen, Malte"
    assert written["titles"] == ["CNRM-CM6-1 GHG concentrations"]
    assert (
        written["subjects"][0]["subject"]
        == "CMIP6.DCPP.CNRM-CERFACS.CNRM-CM6-1.dcppA-hindcast"
    )

    remove(expected_file)
