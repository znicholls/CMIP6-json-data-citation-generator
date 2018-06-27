from os.path import join
import sys

import pytest
from mock import patch

from CMIP6_json_data_citation_generator.upload_CMIP6_json_files import main
from CMIP6_json_data_citation_generator.upload_CMIP6_json_files import upload

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

@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.get_files_to_upload')
def test_all_switch(mock_get_files_to_upload):
    assert True
