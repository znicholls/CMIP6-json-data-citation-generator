from os import listdir, makedirs
from os.path import split, splitext, basename, join, isdir, isfile

import yaml
import json

class CMIPPathHandler():
    def __init__(self):
        self._path_to_handle = ''
        self._fn_ids = [
            'variable_id',
            'activity_id',
            'dataset_category',
            'target_mip',
            'source_id',
            'grid_label',
            'time_id',
            'institution_id',
            'scenario_id',
            'version_number',
            'extension',
        ]

    def get_split_CMIP6_filename(self, file_name=None):
        filename, ext = splitext(basename(file_name))
        filename_bits = {
            self._fn_ids[i]: fn_attribute
            for i, fn_attribute in enumerate(filename.split('_'))
        }
        filename_bits['file_type'] = ext

        try:
            source_id_parts = filename_bits['source_id'].split('-')
        except KeyError:
            raise ValueError('Unable to split filename: {}'.format(filename + ext))

        filename_bits['institution_id'] = source_id_parts[0]
        filename_bits['version_number'] = '-'.join(source_id_parts[-3:])
        if 'ssp' in filename_bits['source_id']:
            filename_bits['scenario_id'] = '-'.join(source_id_parts[1:-3])
        else:
            filename_bits['scenario_id'] = 'N/A'

        return filename_bits

class jsonGenerator():
    def __init__(self):
        self.unique_scenario_ids = []
        self.source_id_written_for = []
        self.valid_yaml_path = join(
            split(__file__)[0], '..',
            'tests', 'data', 'yaml-test-files',
            'test-data-citation-template.yml'
        )

    def get_unique_source_ids_in_dir(self, dir_to_search=None):
        self.unique_scenario_ids = []
        self.add_unique_source_ids_in_dir_to_unique_scenario_ids(dir_to_add=dir_to_search)
        return self.unique_scenario_ids

    def add_unique_source_ids_in_dir_to_unique_scenario_ids(self, dir_to_add=None):
        for file_name in listdir(dir_to_add):
            if file_name.endswith('.nc'):
                try:
                    source_id = self.split_CMIP6_filename(file_name)['source_id']
                    if source_id not in self.unique_scenario_ids:
                        self.unique_scenario_ids.append(source_id)
                except ValueError as invalid_name_exception:
                    print(invalid_name_exception)

    def split_CMIP6_filename(self, file_name=None):
        PathHandler = CMIPPathHandler()
        return PathHandler.get_split_CMIP6_filename(file_name=file_name)

    def return_template_yaml_from(self, in_file=None):
        return yaml.load(open(in_file, 'r'))

    def check_yaml_template(self, yaml_template=None, original_file=None):
        valid_yaml = self.return_template_yaml_from(
            in_file=self.valid_yaml_path
        )
        self.check_all_values_valid(
            yaml_to_check=yaml_template,
            yaml_correct=valid_yaml,
            original_file=original_file
        )

    def check_all_values_valid(self, yaml_to_check=None, yaml_correct=None, original_file=None):
        optional_keys = ['fundingReferences', 'relatedIdentifiers']
        for key in yaml_correct:
            if key not in yaml_to_check:
                if key in optional_keys:
                    msg = 'The key, {}, is missing in your yaml file: {}\nDo you want to add it?'.format(
                        key,
                        original_file,
                    )
                    print(msg)
                else:
                    error_msg = 'The key, {}, is missing in your yaml file: {}'.format(
                        key,
                        original_file,
                    )
                    raise KeyError(error_msg)

        for key, value in yaml_to_check.items():
            if key not in yaml_correct:
                error_msg = 'The key, {}, looks wrong (either it should not be there or is a typo) in your yaml file: {}'.format(
                    key,
                    original_file,
                )
                raise KeyError(error_msg)
            if isinstance(value, dict):
                self.check_all_values_valid(
                    yaml_to_check=value,
                    yaml_correct=yaml_correct[key]
                )
            else:
                if type(value) != type(yaml_correct[key]):
                    error_msg = 'The type ({}) of key, {}, looks wrong in your yaml file: {}\nI think it should be a {}'.format(
                        type(value),
                        key,
                        original_file,
                        type(yaml_correct[key]),
                    )
                    raise ValueError(error_msg)

    def get_yaml_with_filename_values_substituted(self, raw_yml=None, file_name=None):
        def make_substitutions(item):
            filename_bits = self.split_CMIP6_filename(file_name=file_name)
            if isinstance(item, str):
                for key, value in filename_bits.items():
                    item = item.replace(
                        '<' + key + '>',
                        value
                    )
                return item
            elif isinstance(item, list):
                return [make_substitutions(value) for value in item]
            elif isinstance(item, dict):
                return {key: make_substitutions(value) for key, value in item.items()}

        updated_yml = {}
        for key, value in raw_yml.items():
            updated_yml[key] = make_substitutions(value)

        return updated_yml

    def write_json_to_file(self, json_dict=None, file_name=None):
        with open(file_name, 'w') as file_name:
            json.dump(json_dict, file_name, indent=4)

    def write_json_for_filename_to_file_with_template(self, file_name=None, yaml_template=None, output_file=None):
        yaml_template = self.return_template_yaml_from(in_file=yaml_template)
        self.check_yaml_template(
            yaml_template=yaml_template,
            original_file=file_name
        )
        yaml_substituded = self.get_yaml_with_filename_values_substituted(
            raw_yml = yaml_template,
            file_name = file_name
        )
        self.write_json_to_file(
            json_dict=yaml_substituded,
            file_name=output_file
        )

    def generate_json_for_all_unique_scenario_ids(self, in_dir=None, out_dir=None, yaml_template=None):
        for file_name in listdir(in_dir):
            if not file_name.endswith('.nc'):
                print('Skipping non-nc file: {}'.format(file_name))
                continue

            file_to_write = join(
                out_dir,
                self.split_CMIP6_filename(file_name=file_name)['source_id'] + '.json'
            )
            if isfile(file_to_write):
                print('json file already exists for source_id, see file: {}\nskipping file: {}'.format(file_to_write, file_name))
                continue

            if not isdir(out_dir):
                print('Made dir: {}'.format(out_dir))
                makedirs(out_dir)

            print('Writing json file: {}\nfor file: {}'.format(file_to_write, file_name))
            self.write_json_for_filename_to_file_with_template(
                file_name=file_name,
                yaml_template=yaml_template,
                output_file=file_to_write,
            )
