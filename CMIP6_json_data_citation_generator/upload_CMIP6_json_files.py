from os import listdir
import argparse

def get_files_to_upload(input_dir, find_all=False):
    return None

def upload(input_dir, upload_all=False):
    files = get_files_to_upload(input_dir, find_all=upload_all)
    return None

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
    print(args)
    upload(input_dir=args.input, upload_all=args.all)

if __name__ == '__main__':
    main()
