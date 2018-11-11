import io
import yaml
import json


from .validators import CitationSchema


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
        raw_dict = yaml.load(stream)

    return validate_and_return_raw_dict(raw_dict, schema=schema)


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
