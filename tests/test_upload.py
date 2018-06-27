from os.path import join

import pytest
import subprocess
from mock import patch

drive_script_path = join('.', 'scripts', 'upload_CMIP6_json_files.py')

# mock list
# mock uploader
# ensure called and print did as expected

# @pytest.fixture()
# def mock_list_uploader(request):
#     return None

# def test_upload(mock_list_uploader):
#     subprocess.check_call([
#         'python',
#         drive_script_path,
#     ])



#     for source_id in test_file_unique_source_ids:
#         expected_output_file = join(test_output_path, source_id + '.json')
#         assert isfile(expected_output_file)

#     rmtree(test_output_path)
