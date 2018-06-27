import argparse

def upload(input_dir, all=False):
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
    upload(input_dir=args.input, all=args.all)

if __name__ == '__main__':
    main()
