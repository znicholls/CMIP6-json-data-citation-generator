import io
import yaml
import json
from copy import deepcopy


from .validators import CitationSchema


def _add_compulsory_subject(input_dict):
    output_dict = deepcopy(input_dict)
    skey = "subjects"
    if skey not in output_dict:
        output_dict[skey] = []

    subject_compulsory_dict = {
        "subject": "<subject>",
        "subjectScheme": "DRS",
        "schemeURI": "http://github.com/WCRP-CMIP/CMIP6_CVs",
    }
    output_dict["subjects"].insert(0, subject_compulsory_dict)

    return output_dict


def load_and_validate_yaml(yaml_to_read, schema=CitationSchema):
    """Load yaml from file and validate using schema

    Parameters
    ----------
    yaml_to_read: str
        File to read the yaml from

    schema: :obj:`marshmallow.Schema`
        Schema to use to validate the loaded yaml

    Returns
    -------
    dict:
        Loaded dictionary which has been validated by ``schema``
    """
    with open(yaml_to_read, "r") as stream:
        raw_dict = yaml.safe_load(stream)

    prepped_dict = _add_compulsory_subject(raw_dict)

    return validate_and_return_raw_dict(prepped_dict, schema=schema)


def validate_and_return_raw_dict(raw_dict, schema=CitationSchema):
    """Return dictionary validated using the ``CitationSchema``

    Parameters
    ----------
    raw_dict: dict
        Raw dictionary to load

    schema: :obj:`marshmallow.Schema`
        Schema to use to validate the dictionary

    Returns
    -------
    dict:
        Loaded dictionary which has been validated by ``schema``
    """
    return CitationSchema().load(raw_dict)


def write_json(json_dict, path):
    """Write json file from input dictionary to path

    Parameters
    ----------
    json_dict: dict
        Dictionary containing the json to write

    path: str
        Path to write to
    """
    with io.open(path, "w", encoding="utf-8") as outfile:
        outfile.write(
            str(json.dumps(json_dict, sort_keys=True, indent=4, ensure_ascii=False))
        )
