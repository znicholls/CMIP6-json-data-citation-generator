from os.path import join, dirname, abspath


from cmip6_data_citation_generator import generate_jsons


here = dirname(abspath(__file__))
generate_jsons(
    join(here, "..", "tests", "test_data", "input4MIPs_like"),
    join(here, "..", "tests", "test_data", "valid_input.yaml"),
    "CMIP6input4MIPs",
    join(here, "..", "output-examples")
)
