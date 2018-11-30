from unittest.mock import patch, MagicMock
import json


from cmip6_data_citation_generator.upload import upload_jsons
from conftest import TEST_VALID_OUTPUT_JSON, TEST_DATA_ROOT_DIR


@patch("cmip6_data_citation_generator.netrc.netrc")
@patch.object("cmip6_data_citation_generator.httplib2.Http", "add_credentials")
@patch.object("cmip6_data_citation_generator.httplib2.Http", "request")
def test_upload_file(mock_request, mock_add_credentials, mock_netrc):
    tlogin = "login"
    tpassword = "pword"

    mock_netrc = MagicMock()
    mock_netrc.authenticators = MagicMock(return_value = (tlogin, "", tpassword))

    res = upload_jsons(TEST_VALID_OUTPUT_JSON)
    assert res == 0

    mock_netrc.assert_called_with("cera")
    mock_add_credentials.assert_called_with(tlogin, tpassword)
    mock_request.assert_called_with(
        "http://ceracite.dkrz.de:5000/api/v1/citation",
        "POST",
        json.dumps(json.load(TEST_VALID_OUTPUT_JSON)),
        headers={"Content-Type": "application/json"}
    )


@patch("cmip6_data_citation_generator.netrc.netrc")
@patch.object("cmip6_data_citation_generator.httplib2.Http", "add_credentials")
@patch.object("cmip6_data_citation_generator.httplib2.Http", "request")
def test_upload_dir(mock_request, mock_add_credentials, mock_netrc):
    tlogin = "login"
    tpassword = "pword"

    mock_netrc = MagicMock()
    mock_netrc.authenticators = MagicMock(return_value = (tlogin, "", tpassword))

    res = upload_jsons(TEST_DATA_ROOT_DIR, test=True)
    assert res == 0

    mock_netrc.assert_called_with("cera")
    mock_add_credentials.assert_called_with(tlogin, tpassword)
    mock_request.assert_called_with(
        "http://ceracite.dkrz.de:5000/api/v1/citation?test=1",
        "POST",
        json.dumps(json.load(TEST_VALID_OUTPUT_JSON)),
        headers={"Content-Type": "application/json"}
    )

