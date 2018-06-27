from os.path import join, isdir
import sys

import pytest
from mock import patch

from CMIP6_json_data_citation_generator.upload_CMIP6_json_files import main
from CMIP6_json_data_citation_generator.upload_CMIP6_json_files import upload
from CMIP6_json_data_citation_generator.upload_CMIP6_json_files import get_files_to_upload

command_line_command = "upload_CMIP6_json_files"

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

@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.get_files_to_upload')
def test_upload_passing(mock_get_files_to_upload):
    upload('test/input')
    mock_get_files_to_upload.assert_called_with("test/input", find_all=False)
    upload('test/input', upload_all=True)
    mock_get_files_to_upload.assert_called_with("test/input", find_all=True)

@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.listdir')
def test_get_files_to_upload(mock_listdir):
    test_dir = 'input/dir'
    test_files = ['a', 'b', 'c']
    def mock_listdir_return(in_dir):
        if in_dir == test_dir:
            return test_files
        else:
            return []

    mock_listdir.side_effect = mock_listdir_return
    assert test_files == get_files_to_upload(test_dir, find_all=True)
    assert ['a'] == get_files_to_upload(test_dir, find_all=False)

    junk_dir = './junk/dir'
    assert not isdir(junk_dir)
    assert [] == get_files_to_upload(junk_dir, find_all=True)

@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.get_files_to_upload')
@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.subprocess')
def test_upload_call(mock_subprocess, mock_get_files_to_upload):
    test_files = ['a', 'b', 'c']
    mock_get_files_to_upload.return_value = test_files
    expected_client_file = __file__.replace(
        join('tests', 'test_upload.py'),
        join('CMIP6_json_data_citation_generator', 'upload_CMIP6_json_files.py', '..', 'dkrz_citation_api_client', 'citation_client.py')
    )

    upload('irrelevant')
    assert mock_subprocess.check_call.call_count == 3
    for test_file in test_files:
        mock_subprocess.check_call.assert_any_call([
            'python',
            expected_client_file,
            test_file,
        ])
