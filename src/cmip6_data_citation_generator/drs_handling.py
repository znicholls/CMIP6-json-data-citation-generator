import os
import re


from netcdf_scm.iris_cube_wrappers import CMIP6Input4MIPsCube, CMIP6OutputCube


def _get_unique_subjects_in_dir(directory, drs, regexp=".*"):
    """Get unique subjets in directory.

    This returns all the unique data citation subjects from the files in a directory.

    Parameters
    ----------
    directory : str
        Directory to search (includes all sub-directories).

    drs : str
        The data reference syntax used to save your data. Must be one of
        ["CMIP6input4MIPS", "CMIP6output"].

    regexp : str
        Regular expression to use to filter the found filepaths. Only filepaths which
        match this regular expression will be used to generate the unique subjects
        list.
    """
    regexp = re.compile(regexp)
    matching_paths = []
    for root, dirs, files in os.walk(directory):
        full_paths = [os.path.join(root, f) for f in files]
        mps = [fp for fp in full_paths if regexp.match(fp) and fp]
        if mps:
            [matching_paths.append(mp) for mp in mps]

    drs_funcs = {
        "CMIP6output": _get_subject_cmip6output_path,
        "CMIP6input4MIPs": _get_subject_cmip6input4mips_path,
    }
    for key, value in drs_funcs.items():
        if drs == key:
            subjects = []
            for mpath in matching_paths:
                subject = value(mpath)
                if subject not in subjects:
                    subjects.append(subject)

            return sorted(subjects)

    raise ValueError("drs must be one of: {}".format(list(drs_funcs.keys())))


def _get_subject_cmip6input4mips_path(path):
    drs_cube = CMIP6Input4MIPsCube()
    ids = drs_cube.get_load_data_from_identifiers_args_from_filepath(path)

    return "{activity_id}.{mip_era}.{target_mip}.{institution_id}.{source_id}".format(
        **ids
    )


def _get_subject_cmip6output_path(path):
    drs_cube = CMIP6OutputCube()
    ids = drs_cube.get_load_data_from_identifiers_args_from_filepath(path)

    return "{mip_era}.{activity_id}.{institution_id}.{source_id}".format(**ids)
