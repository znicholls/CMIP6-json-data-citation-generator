def _get_unique_subjects_in_dir(directory, drs, regexp="*."):
    """Get unique subjets in directory.

    This returns all the unique data citation subjects from the files in a directory.

    Parameters
    ----------
    directory : str
        Directory to search.

    drs : str
        The data reference syntax used to save your data. Must be one of
        ["CMIP6input4MIPS", "CMIP6output"].

    regexp : str
        Regular expression to use to filter the found filepaths. Only filepaths which
        match this regular expression will be used to generate the unique subjects
        list.
    """
    pass
