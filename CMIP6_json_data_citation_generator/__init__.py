from os import listdir
from os.path import splitext, basename

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
                except Exception:
                    pass

    def split_CMIP6_filename(self, file_name=None):
        PathHandler = CMIPPathHandler()
        return PathHandler.get_split_CMIP6_filename(file_name=file_name)
