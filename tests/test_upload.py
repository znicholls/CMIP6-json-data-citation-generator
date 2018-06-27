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

@patch('CMIP6_json_data_citation_generator.listdir')
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
    assert 1 == len(get_files_to_upload(test_dir, find_all=False))

    junk_dir = './junk/dir'
    assert not isdir(junk_dir)
    assert [] == get_files_to_upload(junk_dir, find_all=True)
