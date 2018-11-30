import sys
import argparse


from .upload import upload_jsons


def upload():
    parser = argparse.ArgumentParser(
        prog="upload-cmip6-citation-files",
        description="Upload citation json files to the CMPI6 data citation service.",
    )

    input_help = (
        "File or folder of files to upload. If input is a folder, "
        "upload-cmip6-citation-files will attempt to upload all `.json` files found "
        "in the folder."
    )
    parser.add_argument(
        "input",
        help=input_help
    )
    parser.add_argument(
        "-t", "--test", help="Do a test run", action="store_true"
    )

    args = parser.parse_args()

    any_error = upload_jsons(
        args.input,
        test=args.test,
    )

    sys.exit(any_error)
