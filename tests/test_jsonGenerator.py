from os import listdir
from os.path import join
import re
import datetime

from pytest import raises
from mock import patch

from CMIP6_json_data_citation_generator import CMIPPathHandler

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
test_data_citation_template_yaml = join(
    test_file_path_yaml,
    'test-data-citation-template.yml'
)

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
            dir_to_search='.'
            # safe to use because if there's nc files in top level, something is wrong
        )
        mock_split_filename.assert_not_called()

def test_yaml_read_in():
    Generator = jsonGenerator()
    yaml_template = join(test_file_path_yaml, 'test-yaml.yml')
    actual_result = Generator.return_template_yaml_from(in_file=yaml_template)
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

def test_read_yaml_template():
    Generator = jsonGenerator()
    actual_result = Generator.return_template_yaml_from(
        in_file=test_data_citation_template_yaml
    )
    expected_result = {
        'creators': [
            {
                'creatorName': "Last, First A. B.",
                'givenName': "First A. B.",
                'familyName': "Last",
                'email': "email@test.com",
                'nameIdentifier': {
                    'schemeURI': "http://orcid.org/",
                    'nameIdentifierScheme': "ORCID",
                    'pid': "0000-1111-2222-3333",
                },
            },
            {
                'creatorName': "La, Fir",
                'givenName': "Fir",
                'familyName': "La",
                'email': "email2@test.com",
                'nameIdentifier': {
                    'schemeURI': "http://orcid.org/",
                    'nameIdentifierScheme': "ORCID",
                    'pid': "9876-5432-1098-7654",
                },
            },
        ],
        'titles': [
            "activity-id.CMIP-era.targetMIP.institutionID.source-id",
        ],
        'subjects': [
            {
                'subject': "activity-id.CMIP-era.targetMIP.institutionID.source-id",
                'schemeURI': "http://github.com/WCRP-CMIP/CMIP6_CVs",
                'subjectScheme': "DRS",
            },
            {'subject': "forcing data"},
            {'subject': "CMIP6"},
            {'subject': "climate"},
        ],
        'descriptions': [
            {
                'descriptionType': "Abstract",
                'text': 'A bunch of text can go here on multiple lines and will be joined together\n',
            }
        ]
    }
    assert actual_result == expected_result

def test_check_yaml_template():
    Generator = jsonGenerator()
    valid_yml = Generator.return_template_yaml_from(
        in_file=test_data_citation_template_yaml
    )

    key_to_exclude = 'titles'
    missing_title_yml = {
        key: value for key, value in valid_yml.items()
        if key not in key_to_exclude
    }
    error_msg = 'The key, {}, is missing in your yaml file: {}'.format(
        key_to_exclude,
        test_data_citation_template_yaml
    )
    with raises(KeyError, match=re.escape(error_msg)):
        Generator.check_yaml_template(
            yaml_template=missing_title_yml,
            original_file=test_data_citation_template_yaml,
        )

    key_to_add = 'extra key'
    extra_key_yml = valid_yml.copy()
    extra_key_yml[key_to_add] = 15
    error_msg = 'The key, {}, looks wrong (either it should not be there or is a typo) in your yaml file: {}'.format(
        key_to_add,
        test_data_citation_template_yaml
    )
    with raises(KeyError, match=re.escape(error_msg)):
        Generator.check_yaml_template(
            yaml_template=extra_key_yml,
            original_file=test_data_citation_template_yaml,
        )

    key_to_alter = 'titles'
    altered_value = "title string"
    wrong_format_yml = valid_yml.copy()
    wrong_format_yml[key_to_alter] = altered_value
    error_msg = 'The type ({}) of key, {}, looks wrong in your yaml file: {}\nI think it should be a {}'.format(
        type(altered_value),
        key_to_alter,
        test_data_citation_template_yaml,
        type(valid_yml[key_to_alter])
    )
    with raises(ValueError, match=re.escape(error_msg)):
        Generator.check_yaml_template(
            yaml_template=wrong_format_yml,
            original_file=test_data_citation_template_yaml,
        )

def test_check_yaml_replace_values():
    Generator = jsonGenerator()
    valid_yml = Generator.return_template_yaml_from(
        in_file=test_data_citation_template_yaml
    )

    file_name = listdir(test_file_path_empty_files)[0]
    PathHandler = CMIPPathHandler()

    # no substitutions if they're not there
    subbed_yml = Generator.get_yaml_with_filename_values_substituted(
        raw_yml=valid_yml,
        file_name=file_name,
    )
    assert subbed_yml == valid_yml

    for key, value in PathHandler.get_split_CMIP6_filename(file_name=file_name).items():
        valid_yml['titles'] = ['<' + key + '>']
        subbed_yml = Generator.get_yaml_with_filename_values_substituted(
            raw_yml=valid_yml,
            file_name=file_name,
        )
        assert subbed_yml['titles'] == [value]

    for key, value in PathHandler.get_split_CMIP6_filename(file_name=file_name).items():
        valid_yml['subjects'][0]['subject'] = ['<' + key + '>']
        subbed_yml = Generator.get_yaml_with_filename_values_substituted(
            raw_yml=valid_yml,
            file_name=file_name,
        )
        assert subbed_yml['subjects'][0]['subject'] == [value]


@patch('CMIP6_json_data_citation_generator.isdir', return_value=False)
@patch('CMIP6_json_data_citation_generator.makedirs')
@patch.object(jsonGenerator, 'return_template_yaml_from')
@patch.object(jsonGenerator, 'check_yaml_template')
@patch.object(jsonGenerator, 'get_yaml_with_filename_values_substituted')
@patch.object(jsonGenerator, 'write_json_to_file')
@patch('CMIP6_json_data_citation_generator.print')
def test_writing_steps_called(mock_print, mock_writer, mock_substitute, mock_checker, mock_loader, mock_makedirs, mock_isdir):
    file_name = listdir(test_file_path_empty_files)[0]
    PathHandler = CMIPPathHandler()
    source_id = PathHandler.get_split_CMIP6_filename(
        file_name=file_name
    )['source_id']
    file_name_to_write = source_id + '.json'

    Generator = jsonGenerator()
    Generator.write_json_for_filename_with_template(
        file_name=file_name,
        yaml_template=test_data_citation_template_yaml,
        output_path=test_output_path,
    )
    mock_isdir.assert_called_with(test_output_path)
    mock_print.assert_any_call('Made dir: {}'.format(test_output_path))
    mock_makedirs.assert_called_with(test_output_path)
    mock_loader.assert_called_with(in_file=file_name)
    mock_checker.assert_called_with(
        yaml_template=mock_loader(),
        original_file=file_name
    )
    mock_substitute.assert_called_with(
        raw_yml=mock_loader(),
        file_name=file_name
    )
    mock_writer.assert_called_with(
        json_dict=mock_substitute(),
        file_name=join(test_output_path, file_name_to_write)
    )
    expected_file = join(test_output_path, file_name_to_write)
    mock_print.assert_any_call(
        'Writing json file: {}\nfor file: {}'.format(expected_file,
                                                      file_name)
    )
    assert mock_print.call_count == 2

    with patch('CMIP6_json_data_citation_generator.isdir', return_value=True) as mock_isdir:
        Generator.write_json_for_filename_with_template(
            file_name=file_name,
            yaml_template=test_data_citation_template_yaml,
            output_path=test_output_path,
        )
        assert mock_isdir.call_count == 1
        assert mock_loader.call_count == 3
        assert mock_checker.call_count == 1
        assert mock_substitute.call_count == 2
        assert mock_writer.call_count == 1
        assert mock_print.call_count == 2
