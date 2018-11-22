import os
import re


from netcdf_scm.iris_cube_wrappers import CMIP6Input4MIPsCube, CMIP6OutputCube


def _get_unique_subjects_in_dir(directory, drs, regexp=".*", keep=True):
    """Get unique subjets in directory.

    This returns all the unique data citation subjects from the files in a directory.

    Parameters
    ----------
    directory : str
        Directory to search (includes all sub-directories).

    drs : str
        The data reference syntax used to save your data. Must be one of
        ["CMIP6input4MIPs", "CMIP6output"].

    regexp : str
        Regular expression to use to filter the found filepaths.

    keep : bool
        If True, keep the filepaths which match regexp to generate the unique subjects
        list. If False, keep the filepaths which don't match regexp to generate the
        unique subjects list.
    """
    matching_paths = _get_matching_paths_in_dir(directory, regexp=regexp, keep=keep)

    subjects = []
    for mpath in matching_paths:
        try:
            subject = _get_subject_path(mpath, drs)
        except ValueError as exc:
            error_msg = (
                str(exc) + "\n\n"
                "Please note: "
                "The CMIP6 data citation json generator only works with "
                "filepaths which match a CMIP data reference syntax. Hence "
                "we can't make a citation for you unless your files are "
                "correctly named and sorted into appropriate directories. We "
                "are considering upgrading so that citations can be made "
                "independent of filename and directory structure. If this "
                "functionality would be useful, please comment on this issue: "
                "https://github.com/znicholls/CMIP6-json-data-citation-generator/issues/20"
            )
            raise ValueError(error_msg)

        if subject not in subjects:
            subjects.append(subject)

    return sorted(subjects)


def _get_matching_paths_in_dir(directory, regexp=".*", keep=True):
    """Get paths which match regexp in directory recursively.

    Parameters
    ----------
    directory : str
        Directory to search (includes all sub-directories).

    regexp : str
        Regular expression to use to filter the found filepaths.

    keep : bool
        If True, keep the filepaths which match regexp. If False, keep the filepaths
        which don't match regexp.
    """
    regexp = re.compile(regexp)
    matching_paths = []
    for root, _, files in os.walk(directory):
        full_paths = [os.path.join(root, f) for f in files]
        if keep:
            mps = [fp for fp in full_paths if regexp.match(fp) and fp]
        else:
            mps = [fp for fp in full_paths if not regexp.match(fp) and fp]
        if mps:
            matching_paths += mps

    return matching_paths


def _get_ids_path(path, drs):
    processor = _get_path_processor(drs)["ids"]
    return processor(path)


def _get_subject_path(path, drs):
    processor = _get_path_processor(drs)["subject"]
    return processor(path)


def _get_path_processor(drs):
    drs_funcs = {
        "CMIP6output": {
            "subject": _get_subject_cmip6output_path,
            "ids": _get_ids_cmip6output_path,
        },
        "CMIP6input4MIPs": {
            "subject": _get_subject_cmip6input4mips_path,
            "ids": _get_ids_cmip6input4mips_path,
        },
    }

    for key, value in drs_funcs.items():
        if drs == key:
            return value

    raise KeyError("drs must be one of: {}".format(list(drs_funcs.keys())))


def _get_subject_cmip6input4mips_path(path):
    ids = _get_ids_cmip6input4mips_path(path)

    return "{activity_id}.{mip_era}.{target_mip}.{institution_id}.{source_id}".format(
        **ids
    )


def _get_ids_cmip6input4mips_path(path):
    drs_cube = CMIP6Input4MIPsCube()
    return drs_cube.get_load_data_from_identifiers_args_from_filepath(path)


def _get_subject_cmip6output_path(path):
    ids = _get_ids_cmip6output_path(path)

    return "{mip_era}.{activity_id}.{institution_id}.{source_id}.{experiment_id}".format(
        **ids
    )


def _get_ids_cmip6output_path(path):
    drs_cube = CMIP6OutputCube()
    return drs_cube.get_load_data_from_identifiers_args_from_filepath(path)
