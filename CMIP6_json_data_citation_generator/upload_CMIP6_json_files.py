from os import listdir
from os.path import abspath, join, isfile, expanduser
import argparse
import subprocess

from CMIP6_json_data_citation_generator import jsonGenerator

def get_files_to_upload(input_dir, find_all=False):
    checker = jsonGenerator
    files_in_dir = [
        f for f in listdir(input_dir)
        if checker.check_json_format(join(input_dir, f))
    ]

    if find_all:
        return files_in_dir
    else:
        return files_in_dir[:1]

def upload(input_dir, upload_all=False):
    if not isfile(expanduser('~/.netrc')):
        raise ValueError(
            'You need a credentials file before you can upload files, see section 2.1 of http://cera-www.dkrz.de/docs/pdf/CMIP6_Citation_Userguide.pdf'
        )
    files_to_upload = get_files_to_upload(input_dir, find_all=upload_all)
    client_file = join(
        abspath(__file__),
        '../dkrz_citation_api_client/citation_client.py',
    )
    for file_to_upload in files_to_upload:
        subprocess.check_call([
            'python',
            client_file,
            file_to_upload
        ])

def main():
    description = 'Upload json files for CMIP6 GHG concentration projection files to data citation server'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "--all",
        action='store_true',
        help="Upload all files in input directory"
    )
    parser.add_argument(
        "input",
        type=str,
        help="Directory from which to upload files"
    )

    args = parser.parse_args()

    if not args.all:
        print(
            '-------------------------- Note --------------------------\n'
            'By default, this script only uploads one file.\n'
            'This acts as a test before you upload all your citations.\n'
            'To upload all your files, use the --all flag.\n'
            '----------------------------------------------------------\n'
        )

    upload(input_dir=args.input, upload_all=args.all)

if __name__ == '__main__':
    main()
