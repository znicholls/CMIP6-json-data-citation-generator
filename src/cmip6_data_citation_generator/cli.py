import sys
import argparse


from .upload import upload_jsons
from . import generate_jsons


def generate():
    parser = argparse.ArgumentParser(
        prog="generate-cmip6-citation-files",
        description="Generate citation json files for the CMPI6 data citation service.",
    )

    # TODO: find a way to not have to duplicate help
    parser.add_argument("input", help="Directory to search for files")
    parser.add_argument(
        "template", help="Template .yaml file to use as template for citation files"
    )
    parser.add_argument(
        "output", help="Directory in which to save generated json files"
    )
    parser.add_argument(
        "--drs",
        default="CMIP6output",
        choices=["CMIP6input4MIPs", "CMIP6output"],
        help="Data reference syntax the files comply with",
    )
    parser.add_argument(
        "--regexp", help="Regular expression to use to filter files", default=".*"
    )
    parser.add_argument(
        "--keep",
        help="Generate jsons for the files which match the regular expression.",
        dest="keep",
        action="store_true",
    )
    parser.add_argument(
        "--drop",
        dest="keep",
        help="Generate jsons for the files which do not match the regular "
        "expression.",
        action="store_false",
    )
    parser.set_defaults(keep=True)

    args = parser.parse_args()

    generate_jsons(
        args.input,
        args.template,
        args.drs,
        args.output,
        regexp=args.regexp,
        keep=args.keep,
    )

    sys.exit(0)


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
    parser.add_argument("input", help=input_help)
    parser.add_argument("-t", "--test", help="Do a dry run", action="store_true")

    args = parser.parse_args()

    any_error = upload_jsons(args.input, test=args.test)

    sys.exit(any_error)
