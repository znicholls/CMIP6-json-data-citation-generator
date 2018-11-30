from unittest.mock import patch


from cmip6_data_citation_generator.cli import upload


@patch("cmip6_data_citation_generator.cli.sys")
@patch("cmip6_data_citation_generator.cli.argparse.ArgumentParser")
@patch("cmip6_data_citation_generator.cli.upload_jsons")
def test_cli(mock_upload_jsons, mock_argparser, mock_sys):
    class TArgs:
        def __init__(self):
            self.input = "tinput"
            self.test = True

    targs = TArgs()
    mock_argparser.return_value.parse_args.return_value = targs
    merror = 3

    mock_upload_jsons.return_value = merror

    upload()

    mock_argparser.return_value.parse_args.assert_called()
    mock_upload_jsons.assert_called_with(targs.input, test=targs.test)
    mock_sys.exit.assert_called_with(merror)
