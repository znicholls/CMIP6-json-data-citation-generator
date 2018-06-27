from os import listdir
from os.path import join, isfile, dirname
from shutil import rmtree
import re
import datetime
import sys

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

def get_test_file():
    for test_file in listdir(test_file_path_empty_files):
        if isfile(test_file):
            break
    return test_file

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
            dir_to_search=join(dirname(__file__), '..', 'CMIP6_json_data_citation_generator')
            # safe to use because if there's nc files in the source, something is wrong
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
                'affiliation': 'Some university',
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
                'affiliation': 'Other university',
            },
        ],
        'titles': [
            "activity-id.CMIP-era.targetMIP.institutionID.source-id",
        ],
        'fundingReferences': [
            {'funderName': 'Funder name 1'},
            {'funderName': 'Funder name 2'},
        ],
        'relatedIdentifiers': [
            {
                'relatedIdentifier': 'doi-link',
                'relatedIdentifierType': 'DOI',
                'relationType': 'IsDocumentedBy',
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
    missing_compulsory_field_yml = {
        key: value for key, value in valid_yml.items()
        if key not in key_to_exclude
    }
    error_msg = 'The key, {}, is missing in your yaml file: {}'.format(
        key_to_exclude,
        test_data_citation_template_yaml
    )
    with raises(KeyError, match=re.escape(error_msg)):
        Generator.check_yaml_template(
            yaml_template=missing_compulsory_field_yml,
            original_file=test_data_citation_template_yaml,
        )

    key_to_exclude = 'relatedIdentifiers'
    missing_optional_field_yml = {
        key: value for key, value in valid_yml.items()
        if key not in key_to_exclude
    }
    msg = 'The key, {}, is missing in your yaml file: {}\nDo you want to add it?'.format(
        key_to_exclude,
        test_data_citation_template_yaml
    )
    with patch('CMIP6_json_data_citation_generator.print') as mock_print:
        Generator.check_yaml_template(
            yaml_template=missing_optional_field_yml,
            original_file=test_data_citation_template_yaml,
        )
        if sys.version.startswith('3'):
            # for some reason mocking print is not happy with Python2
            assert mock_print.call_count == 1
            mock_print.assert_called_with(msg)

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

    file_name = get_test_file()
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
        valid_yml['fundingReferences'][0]['funderName'] = ['<' + key + '>']
        subbed_yml = Generator.get_yaml_with_filename_values_substituted(
            raw_yml=valid_yml,
            file_name=file_name,
        )
        assert subbed_yml['fundingReferences'][0]['funderName'] == [value]

def test_write_json_to_file():
    with patch('CMIP6_json_data_citation_generator.open') as mock_open:
        with patch('CMIP6_json_data_citation_generator.json.dump') as mock_json_dump:
            Generator = jsonGenerator()
            test_fn = 'UoM-ssp119-1-1-0'
            test_dict = {'hi': 'test', 'bye': 'another test'}
            Generator.write_json_to_file(json_dict=test_dict, file_name=test_fn)
            mock_open.assert_called_with(test_fn, 'w')
            mock_json_dump.assert_called_once()

@patch.object(jsonGenerator, 'return_template_yaml_from')
@patch.object(jsonGenerator, 'check_yaml_template')
@patch.object(jsonGenerator, 'get_yaml_with_filename_values_substituted')
@patch.object(jsonGenerator, 'write_json_to_file')
def test_writing_steps(mock_writer, mock_substitute, mock_checker, mock_loader):
    test_file = get_test_file()
    PathHandler = CMIPPathHandler()
    source_id = PathHandler.get_split_CMIP6_filename(
        file_name=test_file
    )['source_id']
    file_name_to_write = source_id + '.json'
    yaml_template = test_data_citation_template_yaml
    out_dir = 'not/used'
    expected_out_file = join(out_dir, file_name_to_write)

    Generator = jsonGenerator()
    Generator.write_json_for_filename_to_file_with_template(
        file_name=test_file,
        yaml_template=test_data_citation_template_yaml,
        output_file=expected_out_file,
    )
    mock_loader.assert_called_with(in_file=yaml_template)
    mock_checker.assert_called_with(
        yaml_template=mock_loader(),
        original_file=test_file
    )
    mock_substitute.assert_called_with(
        raw_yml=mock_loader(),
        file_name=test_file
    )
    mock_writer.assert_called_with(
        json_dict=mock_substitute(),
        file_name=expected_out_file
    )

@patch('CMIP6_json_data_citation_generator.listdir')
@patch('CMIP6_json_data_citation_generator.isfile', return_value=False)
@patch('CMIP6_json_data_citation_generator.makedirs')
@patch('CMIP6_json_data_citation_generator.isdir', return_value=False)
@patch('CMIP6_json_data_citation_generator.print')
def test_generate_json_for_all_unique_scenario_ids(mock_print, mock_isdir, mock_makedirs, mock_isfile, mock_listdir):
    test_file = [
        fn for fn in listdir(test_file_path_empty_files)
        if fn.endswith('.nc')
    ][0]
    PathHandler = CMIPPathHandler()
    source_id = PathHandler.get_split_CMIP6_filename(
        file_name=test_file
    )['source_id']
    file_name_to_write = source_id + '.json'
    in_dir = 'patched/over'
    out_dir = 'not/used'
    yaml_template = 'not used'
    expected_out_file = join(out_dir, file_name_to_write)

    mock_listdir.return_value = [test_file]
    with patch.object(jsonGenerator, 'write_json_for_filename_to_file_with_template') as mock_write_json:
        Generator = jsonGenerator()
        Generator.generate_json_for_all_unique_scenario_ids(
            in_dir=in_dir,
            out_dir=out_dir,
            yaml_template=yaml_template,
        )
        mock_listdir.assert_called_with(in_dir)
        mock_isfile.assert_called_with(expected_out_file)
        mock_isdir.assert_called_with(out_dir)
        if sys.version.startswith('3'):
            # for some reason mocking print is not happy with Python2
            mock_print.assert_any_call('Made dir: {}'.format(out_dir))
        if sys.version.startswith('3'):
            # for some reason mocking print is not happy with Python2
            mock_print.assert_any_call(
                'Writing json file: {}\nfor file: {}'.format(expected_out_file,
                                                             test_file)
            )
            assert mock_print.call_count == 2
        mock_write_json.assert_called_with(
            file_name=test_file,
            yaml_template=yaml_template,
            output_file=expected_out_file,
        )

    mock_isfile.return_value = True
    with patch.object(jsonGenerator, 'write_json_for_filename_to_file_with_template') as mock_write_json:
        Generator = jsonGenerator()
        Generator.generate_json_for_all_unique_scenario_ids(
            in_dir=in_dir,
            out_dir=out_dir,
            yaml_template=yaml_template,
        )
        mock_listdir.assert_called_with(in_dir)
        mock_isfile.assert_called_with(expected_out_file)
        if sys.version.startswith('3'):
            # for some reason mocking print is not happy with Python2
            assert mock_print.call_count == 3
            mock_print.assert_any_call(
                'json file already exists for source_id, see file: {}\nskipping file: {}'.format(
                    expected_out_file,
                    test_file
                )
            )
        mock_isdir.assert_called_once()
        mock_write_json.assert_not_called()

@patch('CMIP6_json_data_citation_generator.print')
def test_write_json_to_file_only_runs_on_nc_file(mock_print):
    test_files = [
        'mole-fraction-of-c2f6-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-ssp585-1-1-0_gr1-GMNHSH_2015-2500.csv',
        'mole-fraction-of-so2f2-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-ssp585-1-1-0_gr1-GMNHSH_2015-2500.mat'
    ]
    with patch('CMIP6_json_data_citation_generator.listdir', return_value=test_files) as mock_listdir:
        with patch.object(jsonGenerator, 'write_json_for_filename_to_file_with_template') as mock_write_json:
            Generator = jsonGenerator()
            Generator.generate_json_for_all_unique_scenario_ids(
                in_dir='not/used',
                out_dir='not/used',
                yaml_template='not/used',
            )
            mock_write_json.assert_not_called()
            if sys.version.startswith('3'):
                # for some reason mocking print is not happy with Python2
                assert mock_print.call_count == 2
                for test_file in test_files:
                    mock_print.assert_any_call(
                        'Skipping non-nc file: {}'.format(
                            test_file
                        )
                    )
