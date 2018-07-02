from os import listdir, remove
from os.path import join, isfile, dirname
from shutil import rmtree
import re
import datetime
import sys
from tempfile import mkstemp
from copy import deepcopy

import pytest
from pytest import raises
from mock import patch
import json

from utils import captured_output
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
            {
                'creatorName': "Another university",
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
                    "schemeURI": "http://orcid.org/",
                    "nameIdentifierScheme": "ORCID",
                    "pid": "0000-0002-3849-4339"
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

# use a fixture to fix this
# For each field you need to define:
#   - field (semi-colon separated)
#   - compulsory or not
#   - depends on other fields or not
#   - fixed or not
# and do a test for:
#   - what happens if removed
#   - what happens if modified
#   - what happens if type changes

# test that if called with yml file, subjects not compulsory, if called with json file, subjects compulsory and fixed

def test_check_all_values_valid(test_validation_dict):

    assert False

"""
Tests look like:
- remove field
    - if compulsory, check error thrown
    - otherwise, check message printed including any dependencies
- modify field
    - if fixed, check error thrown
    - otherwise do nothing
- modify type
    - check error thrown
"""




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
            with patch.object(jsonGenerator, 'ensure_subjects_field_in_dict') as mock_ensure_subjects_field:
                Generator = jsonGenerator()
                test_fn = 'UoM-ssp119-1-1-0'
                test_dict = {'hi': 'test', 'bye': 'another test'}
                test_dict_plus_subjects = Generator.ensure_subjects_field_in_dict(
                    in_dict=test_dict,
                )
                Generator.write_json_to_file(json_dict=test_dict, file_name=test_fn)
                mock_open.assert_called_with(test_fn, 'w')
                mock_json_dump.assert_called_with(test_dict_plus_subjects, test_fn, indent=4)
                mock_ensure_subjects_field.assert_called_once()

def test_ensure_subjects_field_in_dict():
    Generator = jsonGenerator()
    valid_yml = Generator.return_template_yaml_from(
        in_file=test_data_citation_template_yaml
    )
    test_result = Generator.ensure_subjects_field_in_dict(in_dict=valid_yml)
    assert test_result['subjects'] == [
        {
          "subject": "CMIP6.VIACSAB.PCMDI.PCMDI-test-1-0",
          "schemeURI": "http://github.com/WCRP-CMIP/CMIP6_CVs",
          "subjectScheme": "DRS"
        },
        {
          "subject": "climate"
        },
        {
          "subject": "CMIP6"
        }
    ]
    with raises(TypeError):
        Generator.ensure_subjects_field_in_dict(in_dict=[1, 2, 3])


@patch.object(jsonGenerator, 'return_template_yaml_from')
@patch.object(jsonGenerator, 'check_yaml_template')
@patch.object(jsonGenerator, 'get_yaml_with_filename_values_substituted')
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
@pytest.fixture
def temp_file():
    handle, tmp_file = mkstemp()
    yield tmp_file
    remove(tmp_file)

def test_check_json_format(temp_file):
    temp_file
    Generator = jsonGenerator()
    valid_yml = Generator.return_template_yaml_from(
        in_file=test_data_citation_template_yaml
    )
    valid_json = json.loads(json.dumps(valid_yml))
    with open(temp_file, 'w') as outfile:
        json.dump(valid_json, outfile)

    assert Generator.check_json_format(temp_file)


    del valid_json['titles']

    with open(temp_file, 'w') as outfile:
        json.dump(valid_json, outfile)

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
