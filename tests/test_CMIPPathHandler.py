from pytest import raises
import re

from CMIP6_json_data_citation_generator import CMIPPathHandler

def test_get_split_CMIP6_filename():
    PathHandler = CMIPPathHandler()
    actual_split = PathHandler.get_split_CMIP6_filename(
        file_name='mole-fraction-of-hfc134aeq-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-ssp245-1-1-0_gr-0p5x360deg_201501-250012.nc'
    )
    expected_split = {
        'variable_id': 'mole-fraction-of-hfc134aeq-in-air',
        'activity_id': 'input4MIPs',
        'dataset_category': 'GHGConcentrations',
        'target_mip': 'ScenarioMIP',
        'source_id': 'UoM-ssp245-1-1-0',
        'grid_label': 'gr-0p5x360deg',
        'time_id': '201501-250012',
        'institution_id': 'UoM',
        'scenario_id': 'ssp245',
        'version_number': '1-1-0',
        'file_type': '.nc',
    }
    assert actual_split == expected_split

    actual_split = PathHandler.get_split_CMIP6_filename(
        file_name='mole-fraction-of-c-c4f8-in-air_input4MIPs_GHGConcentrations_CMIP_UoM-CMIP-1-2-0_gr-0p5x360deg_000001-201412.nc'
    )
    expected_split = {
        'variable_id': 'mole-fraction-of-c-c4f8-in-air',
        'activity_id': 'input4MIPs',
        'dataset_category': 'GHGConcentrations',
        'target_mip': 'CMIP',
        'source_id': 'UoM-CMIP-1-2-0',
        'grid_label': 'gr-0p5x360deg',
        'time_id': '000001-201412',
        'institution_id': 'UoM',
        'scenario_id': 'N/A',
        'version_number': '1-2-0',
        'file_type': '.nc',
    }
    assert actual_split == expected_split

    junk_file_name = 'junk_file_name-missing-stuff_everywhere.txt'
    with raises(ValueError, match=re.escape('Unable to split filename: {}'.format(junk_file_name))):
        PathHandler.get_split_CMIP6_filename(junk_file_name)
