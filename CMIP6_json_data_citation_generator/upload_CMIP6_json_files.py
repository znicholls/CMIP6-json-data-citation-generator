from os import listdir
from os.path import abspath, join
import argparse
import subprocess

def get_files_to_upload(input_dir, find_all=False):
    files_in_dir = listdir(input_dir)
    if find_all:
        return files_in_dir
    else:
        return files_in_dir[:1]

def upload(input_dir, upload_all=False):
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
