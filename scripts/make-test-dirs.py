from os import listdir, makedirs
from os.path import join, dirname


from netcdf_scm.iris_cube_wrappers import CMIP6Input4MIPsCube, CMIP6OutputCube
from cmip6_data_citation_generator.utils import deep_substitute


input_dirs = [
    "/Users/zebedeenicholls/Documents/AGCEC/Data/CMIP6GHGConcentrationHistorical_1_2_0",
    "/Users/zebedeenicholls/Documents/AGCEC/Data/CMIP6GHGConcentrationProjections_1_2_0"
]

test_dir = "/Users/zebedeenicholls/Documents/AGCEC/Misc/CMIP6-json-data-citation-generator/tests/test_data"

ifc = CMIP6Input4MIPsCube()

for input_dir in input_dirs:
    for file in listdir(input_dir):
        base_path = "<activity_id>/CMIP6/<target_mip>/UoM/<source_id>/atmos/<frequency>/<variable_id>/<grid_label>/v20180101/"
        replacement_dict = ifc.get_load_data_from_identifiers_args_from_filepath(
            join(base_path.replace("_", "-"), file)
        )

        replacement_dict["frequency"] = "yr" if len(replacement_dict['time_range']) == 9 else "mon"

        base_path = deep_substitute(base_path, replacement_dict)

        full_path = join(test_dir, "input4MIPs_like", base_path, file)
        try:
            makedirs(dirname(full_path))
        except FileExistsError:
            pass
        with open(full_path, "w") as f:
            f.write("")


cmip6_output_path = join(test_dir, "CMIP6output_like", "CMIP6/DCPP/CNRM-CERFACS/CNRM-CM6-1/dcppA-hindcast/s1960-r2i1p1f3/day/pr/gn/v20160215/pr_day_CNRM-CM6-1_dcppA-hindcast_s1960-r2i1p1f3_gn_198001-198412.nc")
try:
    makedirs(dirname(cmip6_output_path))
except FileExistsError:
    pass
with open(cmip6_output_path, "w") as f:
    f.write("")
