from os.path import join
import re
import datetime

from pytest import raises
from mock import patch

from CMIP6_json_data_citation_generator import jsonGenerator

test_file_path_empty_files = join('.', 'tests', 'data', 'empty-test-files')
test_file_unique_source_ids = [
    'UoM-ssp119-1-1-0',
    'UoM-ssp245-1-1-0',
    'UoM-ssp370-1-1-0',
    'UoM-ssp370lowntcf-1-1-0',
    'UoM-ssp534os-1-1-0',
    'UoM-ssp585-1-1-0',
]
test_output_path = join('.', 'test-json-output-path')

test_file_path_yaml = join('.', 'tests', 'data', 'yaml-test-files')

def test_get_unique_source_ids_in_dir():
    Generator = jsonGenerator()
    unique_ids = Generator.get_unique_source_ids_in_dir(
        dir_to_search=test_file_path_empty_files
    )
    unique_ids.sort()
    test_file_unique_source_ids.sort()
    assert unique_ids == test_file_unique_source_ids

    junk_dir = 'junk-dir-hjlkj'
    expected_msg = re.escape(
        "[Errno 2] No such file or directory: '{}'".format(junk_dir)
    )
    with raises(OSError, match=expected_msg):
        Generator.get_unique_source_ids_in_dir(
            dir_to_search = junk_dir
        )

def test_get_unique_source_ids_in_dir_only_acts_on_nc_files():
    Generator = jsonGenerator()
    with patch.object(Generator, 'split_CMIP6_filename') as mock_split_filename:
        Generator.get_unique_source_ids_in_dir(
            dir_to_search='.' # safe to use because if there's nc files in top level, something is wrong
        )
        mock_split_filename.assert_not_called()

def test_yaml_read_in():
    Generator = jsonGenerator()
    yaml_template = join(test_file_path_yaml, 'test-yaml.yml')
    actual_result = Generator.return_template_yml_from(in_file=yaml_template)
    expected_result = {
        'list-field': ['item1', 'item2'],
        'dict-field-1': 34843,
        'date': datetime.date(2001, 1, 23),
        'nested-dict-1': {
            'given': 'Chris',
            'family': 'Dumars',
            'address': {
                'multi-line-field': '458 Walkman Dr.\nSuite #292\n',
                'city': 'Royal Oak',
                'state': 'MI',
                'postal': 48046,
            },
        },
        'shortcut-copy-of-nested-dict-1-using-id': {
            'given': 'Chris',
            'family': 'Dumars',
            'address': {
                'multi-line-field': '458 Walkman Dr.\nSuite #292\n',
                'city': 'Royal Oak',
                'state': 'MI',
                'postal': 48046
            },
        },
        'list-field-2': [
            {
                'dict-ent-1': 'BL394D',
                'dict-ent-2': 4,
                'description': 'Basketball',
                'price': 450.00
            },
            {
                'dict-ent-1': 'BL4438H',
                'dict-ent-2': 1,
                'description': 'Super Hoop',
                'price': 2392.00
            },
        ],
        'tax': 251.42,
        'total': 4443.52,
        'single-line-text': 'Late afternoon is best. Backup contact is Nancy Billsmer @ 338-4338.\n'
    }
    assert actual_result == expected_result
