# -*- coding: utf-8 -*-

from os import listdir, remove
from os.path import join, isfile, dirname
from shutil import rmtree
import re
import datetime
import sys
from tempfile import mkstemp
import codecs
from copy import deepcopy

import pytest
from pytest import raises
from mock import patch
import json

from utils import captured_output
from CMIP6_json_data_citation_generator import CMIPPathHandler
from CMIP6_json_data_citation_generator import jsonGenerator

test_data_path = join('.', 'tests', 'data')
test_file_path_empty_files = join(test_data_path, 'empty-test-files')
test_file_unique_source_ids = [
    'UoM-ssp119-1-1-0',
    'UoM-ssp245-1-1-0',
    'UoM-ssp370-1-1-0',
    'UoM-ssp370lowntcf-1-1-0',
    'UoM-ssp534os-1-1-0',
    'UoM-ssp585-1-1-0',
]
test_output_path = join('.', 'test-json-output-path')

test_file_path_yaml = join(test_data_path, 'yaml-test-files')
test_data_citation_template_yaml = join(
    test_file_path_yaml,
    'test-data-citation-template.yml'
)
test_file_path_yaml_special_char = join(test_data_path, 'yaml-test-files', 'test-special-char.yml')
test_file_path_yaml_special_char_written = test_file_path_yaml_special_char.replace(
    '.yml',
    '-written.yml'
)

@pytest.fixture
def temp_file():
    handle, tmp_file = mkstemp()
    yield tmp_file
    remove(tmp_file)

@pytest.fixture
def valid_data_citation_dict():
    Generator = jsonGenerator()
    return Generator.return_data_citation_dict_from_yaml(
        in_file=test_data_citation_template_yaml
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
    actual_result = Generator.return_data_citation_dict_from_yaml(in_file=yaml_template)
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
    actual_result = Generator.return_data_citation_dict_from_yaml(
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
            {
                'creatorName': 'Another university',
            },
        ],
        'contributors': [
            {
                'contributorType': "ContactPerson",
                'contributorName': "Jungclaus, John",
                'givenName': "John",
                'familyName': "Jungclaus",
                'email': "jj@gmail.com",
                'nameIdentifier': {
                    'schemeURI': "http://orcid.org/",
                    'nameIdentifierScheme': "ORCID",
                    'pid': "4444-1111-2222-3333",
                },
                'affiliation': 'JJ Uni TU',
            },
            {
                'contributorType': "ResearchGroup",
                'contributorName': "JJ institute for tests",
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

@pytest.fixture
def test_validation_dict():
    return {
        'creators-compulsory-independent': [
            {
                'creatorName-compulsory-independent': "Last, First A. B.",
                'givenName-optional-dependent-familyName-email-affiliation': "First A. B.",
                'familyName-optional-dependent-givenName-email-affiliation': "Last",
                'email-optional-dependent-givenName-familyName-affiliation': "email@test.com",
                'nameIdentifier-optional-independent': {
                    'schemeURI-compulsory-independent': "http://orcid.org/",
                    'nameIdentifierScheme-compulsory-independent': "ORCID",
                    'pid-compulsory-independent': "0000-1111-2222-3333",
                },
                'affiliation-optional-dependent-givenName-familyName-email': 'Some university',
            },
        ],
        'titles-compulsory-independent': [
            "activity-id.CMIP-era.targetMIP.institutionID.source-id",
        ],
        "contributors-optional-independent": [
            {
                "contributorType-compulsory-independent": "ContactPerson",
                "contributorName-compulsory-independent": "Jungclaus, Johann",
                "givenName-optional-dependent-familyName-email-affiliation": "Johann",
                "familyName-optional-dependent-givenName-email-affiliation": "Jungclaus",
                "email-optional-dependent-givenName-familyName-affiliation": "johann.jungclaus@mpimet.mpg.de",
                "nameIdentifier-optional-independent": {
                    "schemeURI-compulsory-independent": "http://orcid.org/",
                    "nameIdentifierScheme-compulsory-independent": "ORCID",
                    "pid-compulsory-independent": "0000-0002-3849-4339"
                },
                "affiliation-optional-dependent-givenName-familyName-email": "Max-Planck-Institut fuer Meteorologie"
            },
        ],
        'fundingReferences-optional-independent': [
            {
                'funderName-compulsory-independent': 'Funder name 1',
                'funderIdentifier-optional-dependent-funderIdentifierType': 'http://hello',
                'funderIdentifierType-compulsory-dependent-funderIdentifier': 'Cross Ref ID',
            },
        ],
        'relatedIdentifiers-optional-independent': [
            {
                'relatedIdentifier-compulsory-independent': 'doi-link',
                'relatedIdentifierType-compulsory-independent': 'DOI',
                'relationType-compulsory-independent': 'IsDocumentedBy',
            }
        ]
    }

def get_valid_dict_from_test_validation_dict(tvd):
    def fix_keys(dict_in):
        dict_out = deepcopy(dict_in)
        for key in dict_in:
            new_key = key.split('-')[0]
            dict_out[new_key] = deepcopy(dict_in[key])
            del dict_out[key]

            if isinstance(dict_out[new_key], dict):
                dict_out[new_key] = fix_keys(dict_out[new_key])

            elif isinstance(dict_out[new_key], list):
                for i, value in enumerate(dict_out[new_key]):
                    if isinstance(value, dict):
                        dict_out[new_key][i] = fix_keys(dict_out[new_key][i])

        return dict_out

    return fix_keys(tvd)

def test_removing_fields_from_valid_data_citation_dict(test_validation_dict, valid_data_citation_dict):
    Generator = jsonGenerator()
    test_file = 'test.yml'
    def test_field_removal(test_dict, key_to_remove):
        del test_dict[actual_key]

        if key.split('-')[1] == 'compulsory':
            error_msg = 'The key, {}, is missing in your yaml file: {}'.format(
                actual_key,
                test_file
            )
            with raises(KeyError, match=re.escape(error_msg)):
                Generator.check_data_citation_dict(test_dict, test_file)
        else:
            if key.split('-')[2] == 'dependent':
                error_msg = 'Given you have one or all of the key(s), {}, the key, {}, is required in your yaml file: {}'.format(
                    ', '.join(key.split('-')[3:]),
                    actual_key,
                    test_file
                )
                with raises(KeyError, match=re.escape(error_msg)):
                    Generator.check_data_citation_dict(test_dict, test_file)
            else:
                expected_msg = 'The key, {}, is missing in your yaml file: {}\nDo you want to add it?'.format(
                    actual_key,
                    test_file
                )
                with captured_output() as (out, err):
                    Generator.check_data_citation_dict(test_dict, test_file)

                assert expected_msg == out.getvalue().strip()

    def check_removing_fields(input_schema_dict):
        for key in input_schema_dict:
            actual_key = key.split('-')[0]
            test_dict = get_valid_dict_from_test_validation_dict(input_schema_dict)
            test_field_removal(test_dict, actual_key)

            if isinstance(input_schema_dict[key], dict):
                check_removing_fields(input_schema_dict[key])

            elif isinstance(input_schema_dict[key], list):
                for value in input_schema_dict[key]:
                    if isinstance(value, dict):
                        check_removing_fields(value)

    check_removing_fields(test_validation_dict)

def test_adding_extra_field_valid_data_citation_dict(valid_data_citation_dict):
    Generator = jsonGenerator()
    test_file = 'test.yml'
    Generator.check_data_citation_dict(valid_data_citation_dict, test_file)

    key_to_add = 'extra key'
    valid_data_citation_dict[key_to_add] = [{'hi': 'bye'}]
    error_msg = 'The key, {}, looks wrong (either it should not be there or is a typo) in your yaml file: {}'.format(
        key_to_add,
        test_data_citation_template_yaml
    )
    with raises(KeyError, match=re.escape(error_msg)):
        Generator.check_data_citation_dict(valid_data_citation_dict, test_file)

def test_altering_type_of_valid_data_citation_dict_field(valid_data_citation_dict):
    Generator = jsonGenerator()
    test_file = 'test.yml'
    def check_altering_fields(valid_dict):
        for key in valid_dict:
            test_dict = deepcopy(valid_dict)
            altered_value = 4
            test_dict[key] = altered_value

            error_msg = 'The type ({}) of key, {}, looks wrong in your yaml file: {}\nI think it should be a {}'.format(
                type(altered_value),
                key,
                test_file,
                type(valid_dict[key])
            )
            with raises(ValueError, match=re.escape(error_msg)):
                Generator.check_data_citation_dict(test_dict, test_file)

            if isinstance(valid_dict[key], dict):
                check_altering_fields(valid_dict[key])

            elif isinstance(valid_dict[key], list):
                for value in valid_dict[key]:
                    if isinstance(value, dict):
                        check_altering_fields(value)

    check_altering_fields(test_validation_dict)

# test addition/checking of subject field
# if yaml file, check_data_citation_dict should automatically add subject field
# if json file, check_data_citation_dict should check the value of the subject field and if it doesn't match
"""
"subjects":
  [
    {
      "subject":"<activity_id>.CMIP6.<target_MIP>.<institution-id>[.<source-id>]",
      "subjectScheme":"DRS"
    },
    {"subject":"climate"},
    {"subject":"CMIP6"},
]
"""
# raise an error

def test_get_data_citation_dict_with_filename_values_substituted(valid_data_citation_dict):
    Generator = jsonGenerator()
    file_name = get_test_file()
    PathHandler = CMIPPathHandler()

    # no substitutions if they're not there
    subbed_yml = Generator.get_data_citation_dict_with_filename_values_substituted(
        raw_dict=valid_data_citation_dict,
        file_name=file_name,
    )
    assert subbed_yml == valid_data_citation_dict

    for key, value in PathHandler.get_split_CMIP6_filename(file_name=file_name).items():
        valid_data_citation_dict['titles'] = ['<' + key + '>']
        subbed_yml = Generator.get_data_citation_dict_with_filename_values_substituted(
            raw_dict=valid_data_citation_dict,
            file_name=file_name,
        )
        assert subbed_yml['titles'] == [value]

    for key, value in PathHandler.get_split_CMIP6_filename(file_name=file_name).items():
        valid_data_citation_dict['fundingReferences'][0]['funderName'] = ['<' + key + '>']
        subbed_yml = Generator.get_data_citation_dict_with_filename_values_substituted(
            raw_dict=valid_data_citation_dict,
            file_name=file_name,
        )
        assert subbed_yml['fundingReferences'][0]['funderName'] == [value]

def test_write_json_to_file():
    with patch('CMIP6_json_data_citation_generator.io.open') as mock_open:
        with patch('CMIP6_json_data_citation_generator.json.dumps') as mock_json_dump:
            Generator = jsonGenerator()
            test_fn = 'UoM-ssp119-1-1-0'
            test_dict = {'hi': 'test', 'bye': 'another test'}
            Generator.write_json_to_file(data_citation_dict=test_dict, file_name=test_fn)
            mock_open.assert_called_with(test_fn, 'w', encoding='utf8')
            mock_json_dump.assert_called_once()

@patch.object(jsonGenerator, 'return_data_citation_dict_from_yaml')
@patch.object(jsonGenerator, 'check_data_citation_dict')
@patch.object(jsonGenerator, 'get_data_citation_dict_with_filename_values_substituted')
@patch.object(jsonGenerator, 'write_json_to_file')
def test_writing_steps(mock_writer, mock_substitute, mock_checker, mock_loader):
    test_file = get_test_file()
    PathHandler = CMIPPathHandler()
    filename_bits = PathHandler.get_split_CMIP6_filename(
        file_name=test_file
    )

    file_name_to_write = '_'.join([
        filename_bits['institution_id'],
        filename_bits['source_id'],
        filename_bits['activity_id'],
        filename_bits['target_mip'] + '.json',
    ])
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
    mock_checker.assert_called_with(mock_loader(), test_file)
    mock_substitute.assert_called_with(
        raw_dict=mock_loader(),
        file_name=test_file
    )
    mock_writer.assert_called_with(
        data_citation_dict=mock_substitute(),
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
    filename_bits = PathHandler.get_split_CMIP6_filename(
        file_name=test_file
    )

    file_name_to_write = '_'.join([
        filename_bits['institution_id'],
        filename_bits['source_id'],
        filename_bits['activity_id'],
        filename_bits['target_mip'] + '.json',
    ])
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
            assert mock_print.call_count == 3
        mock_write_json.assert_any_call(
            file_name=test_file,
            yaml_template=yaml_template,
            output_file=expected_out_file,
        )
        mock_write_json.assert_any_call(
            file_name=test_file,
            yaml_template=yaml_template,
            output_file=expected_out_file.replace('_' + filename_bits['target_mip'], ''),
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
            assert mock_print.call_count == 4
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

def test_check_json_format(temp_file, valid_data_citation_dict):
    Generator = jsonGenerator()
    with open(temp_file, 'w') as outfile:
        json.dump(valid_data_citation_dict, outfile)

    assert Generator.check_json_format(temp_file)


    del valid_data_citation_dict['titles']

    with open(temp_file, 'w') as outfile:
        json.dump(valid_data_citation_dict, outfile)

    expected_msg = (
        "'The key, titles, is missing in your yaml file: {}'".format(temp_file)
    )
    with captured_output() as (out, err):
        Generator.check_json_format(temp_file)

    assert not Generator.check_json_format(temp_file)
    assert expected_msg == out.getvalue().strip()

@patch('CMIP6_json_data_citation_generator.isdir', return_value=True)
@patch('CMIP6_json_data_citation_generator.walk')
def test_invalid_name_in_dir(mock_walk, mock_isdir):
    junk_name = 'junk.nc'
    Generator = jsonGenerator()
    mock_walk.return_value = [('root', ('dir',), ([junk_name]))]
    with captured_output() as (out, err):
        Generator.add_unique_source_ids_in_dir_to_unique_scenario_ids('mocked-out')


    assert 'Unable to split filename: {}'.format(junk_name) == out.getvalue().strip()

def test_special_yaml_read():
    Generator = jsonGenerator()
    actual_result = Generator.return_data_citation_dict_from_yaml(
        in_file=test_file_path_yaml_special_char
    )
    expected_result = {
        'creators': [
            {
                'creatorName': u"Müller, Björn",
                'givenName': u"Björn",
                'familyName': u"Müller",
                'email': u"björnmüller@äéèîç.com",
                'affiliation': u'kæčœ universität von Lände',
            },
        ],
    }
    assert actual_result == expected_result

@pytest.fixture
def remove_written_special_yaml():
    yield None
    if isfile(test_file_path_yaml_special_char_written):
        remove(test_file_path_yaml_special_char_written)

def test_special_yaml_write(remove_written_special_yaml):
    Generator = jsonGenerator()
    dict_to_write = Generator.return_data_citation_dict_from_yaml(
        in_file=test_file_path_yaml_special_char
    )
    Generator.write_json_to_file(
        data_citation_dict=dict_to_write,
        file_name=test_file_path_yaml_special_char_written
    )
    expected_strings = [
        u"Müller, Björn",
        u"Björn",
        u"Müller",
        u"björnmüller@äéèîç.com",
        u"kæčœ universität von Lände",
    ]
    with codecs.open(test_file_path_yaml_special_char_written, "r", "utf-8") as written_file:
        written_text = written_file.read()

        for expected_string in expected_strings:
            assert expected_string in written_text
