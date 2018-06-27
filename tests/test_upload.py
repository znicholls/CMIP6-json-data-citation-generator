from os.path import join
import sys

import pytest
from mock import patch

from CMIP6_json_data_citation_generator.upload_CMIP6_json_files import main

command_line_command = "upload_CMIP6_json_files"
# mock sys.argv
# mock list
# mock uploader
# ensure called and print did as expected

@pytest.fixture
def mock_sys_argv():
    def _mock_sys(return_value):
        return patch.object(sys, 'argv', return_value)

    return _mock_sys

@patch('CMIP6_json_data_citation_generator.upload_CMIP6_json_files.upload')
def test_upload(mock_upload, mock_sys_argv):
    # mock_sys_argv.argv = []
    # main()
    # mock_upload.assert_called_with([])
    # with patch.object(sys, 'argv', ['all']):
    with mock_sys_argv([command_line_command, "test/input"]):
        main()
        mock_upload.assert_called_with(input_dir="test/input", all=False)

    with mock_sys_argv([command_line_command, '--all', 'test/input']):
        main()
        mock_upload.assert_called_with(input_dir="test/input", all=True)
