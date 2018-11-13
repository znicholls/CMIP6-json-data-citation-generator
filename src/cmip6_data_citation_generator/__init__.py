from os import makedirs
from os.path import join, isdir


from .io_dcg import load_and_validate_yaml, write_json
from .drs_handling import _get_matching_paths_in_dir, _get_subject_path, _get_ids_path
from .utils import deep_substitute
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


def generate_jsons(input_dir, template_yaml, drs, output_dir, regexp=".*", keep=True):
    """Generate CMIP6 data citation json files

    Parameters
    ----------
    input_dir : str
        Directory to search for files.

    template_yaml : str
        Path to yaml file to use as a template for generating the json file.

    drs : str
        The data reference syntax used to save your data. Must be one of
        ["CMIP6input4MIPS", "CMIP6output"].

    output_dir : str
        The path in which to save the generated files.

    regexp : str
        Regular expression to use to filter the filepaths found in ``input_dir``.

    keep : bool
        If True, generate jsons for the files in filepaths which match ``regexp``. If
        False, do the opposite i.e. generate jsons for the files in filepaths which
        don't match ``regexp``.
    """
    if not isdir(output_dir):
        print("\n{} does not exist, making it now\n".format(output_dir))
        makedirs(output_dir)

    template_yaml_dict = load_and_validate_yaml(template_yaml)
    subjects_written = []

    for fp in _get_matching_paths_in_dir(input_dir, regexp=regexp, keep=keep):
        subject = _get_subject_path(fp, drs)
        if subject in subjects_written:
            continue

        ids = _get_ids_path(fp, drs)
        ids["subject"] = subject
        json_dict = deep_substitute(template_yaml_dict, ids)
        if json_dict["subjects"][0]["subject"] != subject:
            import pdb

            pdb.set_trace()
            raise NotImplementedError("Should reorder here")

        output_path = join(output_dir, "{}.json".format(subject))
        print("Writing citation file for {} to {}".format(subject, output_path))
        write_json(json_dict, output_path)
        subjects_written.append(subject)

    return None
