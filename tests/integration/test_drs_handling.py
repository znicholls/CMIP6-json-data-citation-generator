import re


import pytest


from conftest import (
    TEST_DATA_ROOT_DIR,
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


def test_get_unique_subjects_in_dir_cmip6input4mips_style_regexp_include():
    result = _get_unique_subjects_in_dir(
        TEST_DATA_CMIP6_INPUT4MIPS_STYLE, "CMIP6input4MIPs", regexp=".*AerChemMIP.*"
    )

    expected = sorted(["input4MIPs.CMIP6.AerChemMIP.UoM.UoM-AIM-ssp370-lowNTCF-1-2-0"])

    assert result == expected


def test_get_unique_subjects_in_dir_cmip6input4mips_style_regexp_exclude():
    result = _get_unique_subjects_in_dir(
        TEST_DATA_CMIP6_INPUT4MIPS_STYLE, "CMIP6input4MIPs", regexp="^((?!IMAGE).)*$"
    )

    expected = sorted(
        [
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


def test_get_unique_subjects_in_dir_cmip6input4mips_style_keep_false():
    result = _get_unique_subjects_in_dir(
        TEST_DATA_CMIP6_INPUT4MIPS_STYLE,
        "CMIP6input4MIPs",
        regexp=".*IMAGE.*",
        keep=False,
    )

    expected = sorted(
        [
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

    expected = sorted(["CMIP6.DCPP.CNRM-CERFACS.CNRM-CM6-1.dcppA-hindcast"])

    assert result == expected


def test_get_unique_subjects_in_dir_flat_style():
    error_msg = (
        r"^.*"
        + "\n\n"
        + re.escape(
            "Please note: "
            "The CMIP6 data citation json generator only works with "
            "filepaths which match a CMIP data reference syntax. Hence "
            "we can't make a citation for you unless your files are "
            "correctly named and sorted into appropriate directories. We "
            "are considering upgrading so that citations can be made "
            "independent of filename and directory structure. If this "
            "functionality would be useful, please comment on this issue: "
            "https://github.com/znicholls/CMIP6-json-data-citation-generator/issues/20"
        )
    )
    with pytest.raises(ValueError, match=error_msg):
        _get_unique_subjects_in_dir(TEST_DATA_FLATTISH_STYLE, "CMIP6input4MIPs")


def test_get_unique_subjects_in_dir_cant_read_error():
    error_msg = (
        r"^.*"
        + "\n\n"
        + re.escape(
            "Please note: "
            "The CMIP6 data citation json generator only works with "
            "filepaths which match a CMIP data reference syntax. Hence "
            "we can't make a citation for you unless your files are "
            "correctly named and sorted into appropriate directories. We "
            "are considering upgrading so that citations can be made "
            "independent of filename and directory structure. If this "
            "functionality would be useful, please comment on this issue: "
            "https://github.com/znicholls/CMIP6-json-data-citation-generator/issues/20"
        )
    )
    with pytest.raises(ValueError, match=error_msg):
        _get_unique_subjects_in_dir(TEST_DATA_ROOT_DIR, "CMIP6input4MIPs")


def test_get_unique_subjects_in_dir_no_drs_error():
    error_msg = r"^.?" + re.escape("drs must be one of: ") + r".*$"
    with pytest.raises(KeyError, match=error_msg):
        _get_unique_subjects_in_dir(TEST_DATA_CMIP6_INPUT4MIPS_STYLE, "junk")
