from os.path import join

from pytest import raises

from CMIP6_json_data_citation_generator import jsonGenerator

test_file_path = join('.', 'data', 'empty-test-files/')
test_file_unique_source_ids = [
    'UoM-ssp119-1-1-0',
    'UoM-ssp245-1-1-0',
    'UoM-ssp370-1-1-0',
    'UoM-ssp370lowntcf-1-1-0',
    'UoM-ssp534os-1-1-0',
    'UoM-ssp585-1-1-0',
]
test_output_path = join('.', 'test-json-output-path')

def test_get_unique_source_ids_in_dir():
    Generator = jsonGenerator()
    unique_ids = Generator.get_unique_source_ids_in_dir(
        dir_to_search=test_file_path
    )
    unique_ids.sort()
    test_file_unique_source_ids.sort()
    assert unique_ids == test_file_unique_source_ids

    with raises(ValueError):
        Generator.get_unique_source_ids_in_dir(
            dir_to_search='junk-dir-hjlkj'
        )
