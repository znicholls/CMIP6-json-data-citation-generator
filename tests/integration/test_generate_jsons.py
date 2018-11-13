from os import remove
from os.path import isfile, basename
import json


from conftest import (
    TEST_DATA_CMIP6_OUTPUT_STYLE,
    TEST_DATA_CMIP6_INPUT4MIPS_STYLE,
    TEST_VALID_INPUT_YAML,
    TEST_SPECIAL_CHAR_YAML,
)
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


def test_get_unique_subjects_in_dir_input4mips_style_with_regexp_False():
    generate_jsons(
        TEST_DATA_CMIP6_INPUT4MIPS_STYLE,
        TEST_VALID_INPUT_YAML,
        "CMIP6input4MIPs",
        ".",
        regexp=".*ScenarioMIP.*",
        keep=False,
    )

    expected_files = [
        "./input4MIPs.CMIP6.AerChemMIP.UoM.UoM-AIM-ssp370-lowNTCF-1-2-0.json",
        "./input4MIPs.CMIP6.CMIP.UoM.UoM-CMIP-1-2-0.json",
    ]
    for expected_file in expected_files:
        assert isfile(expected_file)

        written = json.loads(open(expected_file).read())
        subject = ".".join(basename(expected_file).split(".")[:-1])
        assert written["subjects"][0]["subject"] == subject

        remove(expected_file)


def test_generate_jsons_special_characters():
    generate_jsons(
        TEST_DATA_CMIP6_OUTPUT_STYLE,
        TEST_SPECIAL_CHAR_YAML,
        "CMIP6output",
        ".",
        regexp=".*",
    )

    expected_file = "./CMIP6.DCPP.CNRM-CERFACS.CNRM-CM6-1.dcppA-hindcast.json"

    assert isfile(expected_file)

    written = json.loads(open(expected_file).read())

    assert written["contributors"][0]["email"] == "jäèrömü.çiçùúáßæįł@somewhere.edu.au"
    assert written["contributors"][0]["familyName"] == "Çiçùúáßæįł"
    assert written["contributors"][0]["givenName"] == "Jäèrömü"
    assert written["contributors"][0]["contributorName"] == "Çiçùúáßæįł, Jäèrömü"

    remove(expected_file)
