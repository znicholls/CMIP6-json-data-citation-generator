from os.path import join, isfile
from shutil import rmtree
import subprocess
import pytest

drive_call = 'generate_CMIP6_json_files'
test_file_path_yaml = join(
    '.', 'tests', 'data', 'yaml-test-files',
    'test-data-citation-template.yml'
)
test_file_path = join('.', 'tests', 'data', 'empty-test-files')

test_file_unique_jsons = [
    'UoM_UoM-ssp119-1-1-0_input4MIPs_ScenarioMIP',
    'UoM_UoM-ssp245-1-1-0_input4MIPs_ScenarioMIP',
    'UoM_UoM-ssp370-1-1-0_input4MIPs_ScenarioMIP',
    'UoM_UoM-ssp370lowntcf-1-1-0_input4MIPs_ScenarioMIP',
    'UoM_UoM-ssp534os-1-1-0_input4MIPs_ScenarioMIP',
    'UoM_UoM-ssp585-1-1-0_input4MIPs_ScenarioMIP',
]
test_output_path = './test-json-output-path'

@pytest.fixture
def tear_down_test_path():
    yield None
    print('teardown test_output_path')
    rmtree(test_output_path)

def test_pipeline(tear_down_test_path):
    subprocess.check_call([
        drive_call,
        test_file_path_yaml,
        test_file_path,
        test_output_path
    ])

    for unique_json in test_file_unique_jsons:
        expected_output_file = join(test_output_path, unique_json + '.json')
        assert isfile(expected_output_file)
        assert isfile(expected_output_file.replace('_ScenarioMIP', ''))
