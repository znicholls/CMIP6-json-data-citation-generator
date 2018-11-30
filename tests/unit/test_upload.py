from unittest.mock import patch
import json


import pytest


from cmip6_data_citation_generator.upload import upload_jsons
from conftest import TEST_VALID_OUTPUT_JSON, TEST_DATA_ROOT_DIR


@patch("cmip6_data_citation_generator.upload.netrc")
@patch("cmip6_data_citation_generator.upload.Http")
@pytest.mark.parametrize("tinput", (TEST_VALID_OUTPUT_JSON, TEST_DATA_ROOT_DIR))
@pytest.mark.parametrize("ttest", (True, False))
@pytest.mark.parametrize("tcontent", (b"SUCCESS content", b"junk"))
def test_upload_file(mock_Http, mock_netrc, tinput, ttest, tcontent):
    tlogin = "login"
    tpassword = "pword"

    class TResponse(object):
        status = "status"

    tresponse = TResponse()

    with open(TEST_VALID_OUTPUT_JSON) as f:
        expected_data = json.dumps(json.load(f))

    mock_netrc.return_value.authenticators.return_value = (tlogin, "", tpassword)
    mock_Http.return_value.request.return_value = (tresponse, tcontent)

    res = upload_jsons(tinput, test=ttest)
    if tcontent.decode("utf-8").startswith("SUCCESS") or ttest:
        assert res == 0
    else:
        assert res == 1

    if not ttest:
        expected_dest = "http://ceracite.dkrz.de:5000/api/v1/citation"

        mock_netrc.return_value.authenticators.assert_called_with("cera")
        mock_Http.return_value.add_credentials.assert_called_with(tlogin, tpassword)

        mock_Http.return_value.request.assert_called_with(
            expected_dest,
            "POST",
            expected_data,
            headers={"Content-Type": "application/json"},
        )
