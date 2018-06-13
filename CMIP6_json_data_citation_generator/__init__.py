from os import listdir

class CMIPPathHandler():
    def __init__(self):
        self._path_to_handle = ''

    def get_split_CMIP6_filename(self, file_name=None):
        return {}

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
