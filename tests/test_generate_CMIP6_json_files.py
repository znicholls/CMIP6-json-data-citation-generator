from os.path import join, isfile
from shutil import rmtree
import subprocess

drive_call = 'generate_CMIP6_json_files'
test_file_path_yaml = join(
    '.', 'tests', 'data', 'yaml-test-files',
    'test-data-citation-template.yml'
)
test_file_path = join('.', 'tests', 'data', 'empty-test-files')
test_file_unique_source_ids = [
    'UoM-ssp119-1-1-0',
    'UoM-ssp245-1-1-0',
    'UoM-ssp370-1-1-0',
    'UoM-ssp370lowntcf-1-1-0',
    'UoM-ssp534os-1-1-0',
    'UoM-ssp585-1-1-0',
]
test_output_path = './test-json-output-path'

def test_pipeline():
    subprocess.check_call([
        drive_call,
        test_file_path_yaml,
        test_file_path,
        test_output_path
    ])

    for source_id in test_file_unique_source_ids:
        expected_output_file = join(test_output_path, source_id + '.json')
        assert isfile(expected_output_file)

    rmtree(test_output_path)
