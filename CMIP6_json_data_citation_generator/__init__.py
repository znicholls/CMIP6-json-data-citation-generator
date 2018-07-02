from os import listdir, makedirs, walk
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

    def add_unique_source_ids_in_dir_to_unique_scenario_ids(self, dir_to_add):
        if not isdir(dir_to_add):
            raise OSError("[Errno 2] No such file or directory: '{}'".format(dir_to_add))
        for root, dirs, files in walk(dir_to_add):
            for file_name in files:
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
        self.check_all_values_valid(
            dict_to_check=yaml_template,
            original_file=original_file
        )

    def check_all_values_valid(self, dict_to_check, original_file):
        return None


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
        yaml_substituted = self.get_yaml_with_filename_values_substituted(
            raw_yml = yaml_template,
            file_name = file_name
        )
        self.write_json_to_file(
            json_dict=yaml_substituted,
            file_name=output_file
        )

    def generate_json_for_all_unique_scenario_ids(self, in_dir=None, out_dir=None, yaml_template=None):
        for file_name in listdir(in_dir):
            if not file_name.endswith('.nc'):
                print('Skipping non-nc file: {}'.format(file_name))
                continue

            filename_bits = self.split_CMIP6_filename(file_name=file_name)
            file_name_to_write = '_'.join([
                filename_bits['institution_id'],
                filename_bits['source_id'],
                filename_bits['activity_id'],
                filename_bits['target_mip'] + '.json',
            ])
            file_to_write = join(out_dir, file_name_to_write)

            if isfile(file_to_write):
                print('json file already exists for source_id, see file: {}\nskipping file: {}'.format(file_to_write, file_name))
                continue

            if not isdir(out_dir):
                print('Made dir: {}'.format(out_dir))
                makedirs(out_dir)

            files_to_write = [
                file_to_write,
                file_to_write.replace('_' + filename_bits['target_mip'], '')
            ]
            for fn in files_to_write:
                print('Writing json file: {}\nfor file: {}'.format(fn, file_name))
                self.write_json_for_filename_to_file_with_template(
                    file_name=file_name,
                    yaml_template=yaml_template,
                    output_file=fn,
                )

    def check_json_format(self, file_to_check):
        with open(file_to_check, 'r') as in_file:
            yaml_to_check = yaml.load(
                json.dumps(json.load(in_file))
            )

        try:
            self.check_yaml_template(
                yaml_template=yaml_to_check,
                original_file=file_to_check,
            )
            return True
        except Exception as Except:
            print(str(Except))
            return False
