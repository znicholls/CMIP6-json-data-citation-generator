from os.path import join, dirname, abspath


from cmip6_data_citation_generator import generate_jsons


here = dirname(abspath(__file__))

input_dir = join(here, "..", "tests", "test_data", "input4MIPs_like")
template_yaml = join(here, "..", "tests", "test_data", "valid_input.yaml")
drs = "CMIP6input4MIPs"
output_dir = join(".", "example-outputs")
regexp = ".*"  # i.e. all files
keep = True


generate_jsons(
    input_dir,
    template_yaml,
    drs,
    output_dir,
    regexp=regexp,
    keep=keep
)
