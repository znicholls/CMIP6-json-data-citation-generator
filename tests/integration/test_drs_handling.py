import re


import pytest


from conftest import (
    TEST_DATA_CMIP6_INPUT4MIPS_STYLE,
    TEST_DATA_CMIP6_OUTPUT_STYLE,
    TEST_DATA_FLATTISH_STYLE,
)
from cmip6_data_citation_generator.drs_handling import _get_unique_subjects_in_dir


def test_get_unique_subjects_in_dir_cmip6input4mips_style():
    result = _get_unique_subjects_in_dir(
        TEST_DATA_CMIP6_INPUT4MIPS_STYLE, "CMIP6input4MIPs"
    )

    expected = sorted(
        [
            "input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-IMAGE-ssp119-1-2-0",
            "input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-IMAGE-ssp126-1-2-0",
            "input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-MESSAGE-GLOBIOM-ssp245-1-2-0",
            "input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-AIM-ssp370-1-2-0",
            "input4MIPs.CMIP6.AerChemMIP.UoM.UoM-AIM-ssp370-lowNTCF-1-2-0",
            "input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-GCAM4-ssp434-1-2-0",
            "input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-GCAM4-ssp460-1-2-0",
            "input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-REMIND-MAGPIE-ssp534-over-1-2-0",
            "input4MIPs.CMIP6.ScenarioMIP.UoM.UoM-REMIND-MAGPIE-ssp585-1-2-0",
            "input4MIPs.CMIP6.CMIP.UoM.UoM-CMIP-1-2-0",
        ]
    )

    assert result == expected


def test_get_unique_subjects_in_dir_cmip6output_style():
    result = _get_unique_subjects_in_dir(TEST_DATA_CMIP6_OUTPUT_STYLE, "CMIP6output")

    expected = sorted(["CMIP6.DCPP.CNRM-CERFACS.CNRM-CM6-1"])

    assert result == expected


# def test_get_unique_subjects_in_dir_flat_style():
#     _get_unique_subjects_in_dir(TEST_DATA_CMIP6_INPUT4MIPS_STYLE, "CMIP6input4MIPs")
#     assert False


# def test_get_unique_subjects_in_dir_errors():
#     assert False
#     # nothing found
#     # filename/path unreadable


def test_get_unique_subjects_in_dir_no_drs_error():
    error_msg = r"^" + re.escape("drs must be one of: ") + r".*$"
    with pytest.raises(ValueError, match=error_msg):
        _get_unique_subjects_in_dir(TEST_DATA_CMIP6_INPUT4MIPS_STYLE, "junk")
