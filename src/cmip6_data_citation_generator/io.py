import yaml


from .validators import CitationSchema


def load_template_yaml(yaml_to_read):
    with open(yaml_to_read, "r") as stream:
        raw_dict = yaml.load(stream)

    return CitationSchema(strict=True).load(raw_dict).data
