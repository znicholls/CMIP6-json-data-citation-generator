from os.path import join, isdir
import sys

import pytest
from pytest import raises
from mock import patch
import re

from utils import captured_output
from CMIP6_json_data_citation_generator.upload_CMIP6_json_files import main
from CMIP6_json_data_citation_generator.upload_CMIP6_json_files import upload
from CMIP6_json_data_citation_generator.upload_CMIP6_json_files import get_files_to_upload

command_line_command = "upload_CMIP6_json_files"
doc_url = "http://cera-www.dkrz.de/docs/pdf/CMIP6_Citation_Userguide.pdf"

@pytest.fixture
def mock_sys_argv():
    def _mock_sys(return_value):
        return patch.object(sys, 'argv', return_value)

    return _mock_sys

@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.upload')
def test_upload_command_line_interface(mock_upload, mock_sys_argv):
    with mock_sys_argv([command_line_command, "test/input"]):
        main()
        mock_upload.assert_called_with(input_dir="test/input", upload_all=False)

    with mock_sys_argv([command_line_command, '--all', 'test/input']):
        main()
        mock_upload.assert_called_with(input_dir="test/input", upload_all=True)

@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.isfile', return_value=True)
@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.get_files_to_upload')
def test_upload_passing(mock_get_files_to_upload, mock_isfile):
    if sys.version.startswith('3'):
        with raises(NotImplementedError, match='dkrz_citation_api_client is not python3 compatible'):
            upload('irrelevant')
    else:
        upload('test/input')
        mock_get_files_to_upload.assert_called_with("test/input", find_all=False)
        upload('test/input', upload_all=True)
        mock_get_files_to_upload.assert_called_with("test/input", find_all=True)

@patch('CMIP6_json_data_citation_generator.jsonGenerator.check_json_format')
@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.listdir')
def test_get_files_to_upload(mock_listdir, mock_check_json_format):
    test_dir = 'input/dir'
    test_files = ['a.json', 'b.csv', 'c.json', 'd.json']
    def mock_listdir_side_effect(in_dir):
        if in_dir == test_dir:
            return test_files
        else:
            return []

    mock_listdir.side_effect = mock_listdir_side_effect

    def mock_check_json_format_side_effect(in_file):
        if in_file in [join(test_dir, 'a.json'), join(test_dir, 'c.json')]:
            return True
        else:
            return False
    mock_check_json_format.side_effect = mock_check_json_format_side_effect

    assert ['a.json', 'c.json'] == get_files_to_upload(test_dir, find_all=True)
    assert ['a.json'] == get_files_to_upload(test_dir, find_all=False)

    junk_dir = './junk/dir'
    assert not isdir(junk_dir)
    assert [] == get_files_to_upload(junk_dir, find_all=True)

@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.isfile', return_value=True)
@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.get_files_to_upload')
@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.subprocess')
def test_upload_call(mock_subprocess, mock_get_files_to_upload, mock_isfile):
    test_files = ['a', 'b', 'c']
    mock_get_files_to_upload.return_value = test_files
    expected_client_file = __file__.replace(
        join('tests', 'test_upload.py'),
        join('CMIP6_json_data_citation_generator', 'upload_CMIP6_json_files.py', '..', 'dkrz_citation_api_client', 'citation_client.py')
    )

    if sys.version.startswith('3'):
        with raises(NotImplementedError, match='dkrz_citation_api_client is not python3 compatible'):
            upload('irrelevant')
    else:
        with captured_output() as (out, err):
            upload('irrelevant')
        assert mock_subprocess.check_call.call_count == 3
        for test_file in test_files:
            assert 'Uploading {}'.format(test_file) in out.getvalue().strip()
            mock_subprocess.check_call.assert_any_call([
                'python',
                expected_client_file,
                test_file,
            ])

@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.upload')
def test_warnings(mock_upload, mock_sys_argv):
    warning_GUI_upload =(
        '------------------------ Warning ------------------------\n'
        "If you have not yet done so, add the people, institutes \n"
        "and paper references you use in your yaml files to the \n"
        "data via the GUI as described in section 1.5 (people and\n"
        "institutes) and section 1.6 (paper references) of\n" +
        doc_url + "\n"
        "To silence this message, use the -q flag\n"
        '----------------------------------------------------------\n'
    )
    with captured_output() as (out, err):
        with mock_sys_argv([command_line_command, "test/input"]):
            main()
    expected_output = (
        warning_GUI_upload +
        '-------------------------- Note --------------------------\n'
        'By default, this script only uploads one file.\n'
        'This acts as a test before you upload all your citations.\n'
        'To upload all your files, use the --all flag.\n'
        '----------------------------------------------------------'
    )
    print(out.getvalue().strip())
    assert expected_output == out.getvalue().strip()

    with captured_output() as (out, err):
        with mock_sys_argv([command_line_command, '--all', 'test/input']):
            main()
    assert warning_GUI_upload.strip() == out.getvalue().strip()

    with captured_output() as (out, err):
        with mock_sys_argv([command_line_command, '--all', '-q', 'test/input']):
            main()
    assert '' == out.getvalue().strip()

@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.isfile')
def test_error_if_no_credentials(mock_isfile):
    mock_isfile.return_value = False
    expected_error = re.escape('You need a credentials file before you can upload files, see section 2.1 of ' + doc_url)
    with raises(ValueError, match=expected_error):
        upload('irrelevant')

@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.isfile')
def test_error_if_python3(mock_isfile):
    mock_isfile.return_value = True
    if sys.version.startswith('3'):
        with raises(NotImplementedError, match='dkrz_citation_api_client is not python3 compatible'):
            upload('irrelevant')
    else:
        with raises(OSError):
            upload('irrelevant')
