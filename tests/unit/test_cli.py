from unittest.mock import patch


from cmip6_data_citation_generator.cli import generate, upload


@patch("cmip6_data_citation_generator.cli.sys")
@patch("cmip6_data_citation_generator.cli.argparse.ArgumentParser")
@patch("cmip6_data_citation_generator.cli.generate_jsons")
def test_generate(mock_generate_jsons, mock_argparser, mock_sys):
    class TArgs:
        def __init__(self):
            self.input = "tinput"
            self.template = "ttemplate"
            self.output = "toutput"
            self.drs = "tdrs"
            self.regexp = "tregexp"
            self.keep = False

    targs = TArgs()
    mock_argparser.return_value.parse_args.return_value = targs

    generate()

    mock_argparser.return_value.parse_args.assert_called()
    mock_generate_jsons.assert_called_with(
        targs.input,
        targs.template,
        targs.drs,
        targs.output,
        regexp=targs.regexp,
        keep=targs.keep,
    )
    mock_sys.exit.assert_called_with(0)


@patch("cmip6_data_citation_generator.cli.sys")
@patch("cmip6_data_citation_generator.cli.argparse.ArgumentParser")
@patch("cmip6_data_citation_generator.cli.upload_jsons")
def test_upload(mock_upload_jsons, mock_argparser, mock_sys):
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
