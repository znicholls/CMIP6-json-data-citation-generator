from os.path import join


from .io_dcg import load_and_validate_yaml, write_json
from .drs_handling import _get_matching_paths_in_dir, _get_subject_path, _get_ids_path
from .utils import deep_substitute
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

def generate_jsons(input_dir, template_yaml, drs, output_dir, regexp=".*", keep=True):
    template_yaml_dict = load_and_validate_yaml(template_yaml)
    subjects_written = []

    for fp in _get_matching_paths_in_dir(input_dir, regexp=regexp, keep=keep):
        subject = _get_subject_path(fp, drs)
        if subject in subjects_written:
            continue

        ids = _get_ids_path(fp, drs)
        json_dict = deep_substitute(template_yaml_dict, ids)
        if json_dict["subjects"][0]["subject"] != subject:
            import pdb
            pdb.set_trace()
            raise NotImplementedError("Should reorder here")

        write_json(json_dict, join(output_dir, "{}.json".format(subject)))

    return None
