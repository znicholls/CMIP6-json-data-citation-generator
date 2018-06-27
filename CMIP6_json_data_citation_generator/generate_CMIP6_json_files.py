import argparse
from CMIP6_json_data_citation_generator import jsonGenerator

def main():
    description = 'Generate json files for CMIP6 GHG concentration projection files'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("yamlfile", type=str, help="Path to yaml file to use as template")
    parser.add_argument("inputpath", type=str, help="Path with raw files")
    parser.add_argument("outputpath", type=str, help="Path to output files into")

    args = parser.parse_args()

    yaml_file = args.yamlfile
    input_path = args.inputpath
    output_path = args.outputpath

    Generator = jsonGenerator()
    Generator.generate_json_for_all_unique_scenario_ids(
        in_dir=input_path,
        out_dir=output_path,
        yaml_template=yaml_file,
    )

if __name__ == '__main__':


    main()
