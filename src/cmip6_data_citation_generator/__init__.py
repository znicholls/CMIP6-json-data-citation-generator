from .io_dcg import load_and_validate_yaml
from .drs_handling import _get_matching_paths_in_dir
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

def generate_jsons(input_dir, template_yaml, drs, output_dir, regexp=".*", keep=True):
    template_yaml_dict = load_and_validate_yaml(template_yaml)
    # import pdb
    # pdb.set_trace()
    # get all matching paths in dict
    # loop over, get subject, if subject not there, substitute in yaml, write json
    for fp in _get_matching_paths_in_dir(input_dir, regexp=regexp, keep=keep):
        pass
    return None
