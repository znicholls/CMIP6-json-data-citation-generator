# CMIP6-json-data-citation-generator

[![Build Status](https://img.shields.io/travis/znicholls/CMIP6-json-data-citation-generator.svg)](https://travis-ci.org/znicholls/CMIP6-json-data-citation-generator)

<!-- MarkdownTOC autolink="true" autoanchor="true" markdown_preview="github" -->

- [Notation](#notation)
- [Installation](#installation)
    - [Use](#use)
    - [Development](#development)
- [Usage](#usage)
    - [Summary](#summary)
    - [Example](#example)
    - [Details](#details)
        - [Text Substitutions in yaml Files](#text-substitutions-in-yaml-files)

<!-- /MarkdownTOC -->


Simple scripts to automatically generate json data citations for CMIP6 data files.

<a id="notation"></a>
## Notation

To be written, need to mention that `<name>` indicates that you should replace `<name>` including the `<>` with the appropriate file, variable, path etc.

<a id="installation"></a>
## Installation

<a id="use"></a>
### Use

```
python2 -m virtualenv venv # python3 will also work
source venv/bin/activate
pip install --upgrade pip
pip install -Ur dev-requirements.txt
python setup.py install
```

<a id="development"></a>
### Development

```
make test
```

This will install the virtual environments (both python2 and python3) and run the tests.

<a id="usage"></a>
## Usage

<a id="summary"></a>
### Summary

`json` files for files in the directory, `<input_dir>`, can be generated in the output directory, `<output_dir>`, using a yaml template file, `<yaml_template>` as shown

```
python generate_CMIP6_json_files.py <yaml_template> <input_dir> <output_dir>
```

<a id="example"></a>
### Example

The script will only generate one `json` file for each unique source id it finds in the `<input_dir>`. To see an example, run the following whilst your working directory is `CMIP6-json-data-citation-generator`

```
source venv/bin/activate # if you haven't already
python ./scripts/generate_CMIP6_json_files.py ./examples/yaml-templates/yaml-example.yml ./examples/data/empty-test-files/ ./examples/outputs
```

<a id="details"></a>
### Details

The script loads a template yaml file, which it then uses to write out the `json` files. An example of what this yaml file should look like is in `CMIP6-json-data-citation-generator/examples/yaml-templates/yaml-example.yml`.

*Note:* as explained in the tutorial, you must first use the online GUI to add people and institutions before your `json` files can be used directy with the API. Having said that, the files may be useful in and of themselves if you need a hand from the data citation team.

<a id="text-substitutions-in-yaml-files"></a>
#### Text Substitutions in yaml Files

You will notice that in that file, the `titles` field has a few strings which are wrapped in `<>`. Such strings can be replaced with information from the filename. The available substitutions are:

- variable_id
- activity_id
- dataset_category
- target_mip
- source_id
- grid_label
- time_id
- institution_id
- scenario_id
- version_number
- extension

This expects filenames of the form, `variable-id_activity-id_dataset-category_target-mip_source-id_grid-label_time-idextension`, where `source-id` is composed of `institution-id-scenario-id-version-number`. Two illustrative examples are given below:

For a filename such as, `mole-fraction-of-c2f6-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-ssp119-1-1-0_gn-15x360deg_201501-250012.nc`, the substitutions that will be made are:

- <variable_id> --> mole-fraction-of-c2f6-in-air
- <activity_id> --> input4MIPs
- <dataset_category> --> GHGConcentrations
- <target_mip> --> ScenarioMIP
- <source_id> --> UoM-ssp119-1-1-0
- <grid_label> --> gn-15x360deg
- <time_id> --> 201501-250012
- <institution_id> --> UoM
- <scenario_id> --> ssp119
- <version_number> --> 1-1-0
- <extension> --> .nc

For a filename such as, `mole-fraction-of-methyl-chloride-in-air_input4MIPs_GHGConcentrations_CMIP_UoM-1-1-0_gr1-GMNHSH_000001-201412.nc`, the substitutions that will be made are:

- <variable_id> --> mole-fraction-of-methyl-chloride-in-air
- <activity_id> --> input4MIPs
- <dataset_category> --> GHGConcentrations
- <target_mip> --> CMIP
- <source_id> --> UoM-1-1-0
- <grid_label> --> gr1-GMNHSH
- <time_id> --> 000001-201412
- <institution_id> --> UoM
- <scenario_id> --> N/A
- <version_number> --> 1-1-0
- <extension> --> .nc
