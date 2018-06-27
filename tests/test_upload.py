from os.path import join

import pytest
from mock import patch


# from CMIP6_json_data_citation_generator import upload_CMIP6_json_files

# mock sys.argv
# mock list
# mock uploader
# ensure called and print did as expected

@pytest.fixture
def mock_sys():
    return patch('upload_CMIP6_json_files.sys')


def test_upload(mock_sys):
    mock_sys.argv = []
    print(mock_sys.argv)
    mock_sys.argv = ['--all']
    print(mock_sys.argv)

    mock_upload.assert_not_called()
