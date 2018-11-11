import yaml


from .validators import CitationSchema


def load_template_yaml(yaml_to_read):
    with open(yaml_to_read, "r") as stream:
        raw_dict = yaml.load(stream)

    return validate_and_return_raw_dict(raw_dict)


def validate_and_return_raw_dict(raw_dict):
    return CitationSchema().load(raw_dict)
