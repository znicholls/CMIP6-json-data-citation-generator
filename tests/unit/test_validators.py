from cmip6_data_citation_generator.validators import CitationSchema

def test_load_template_yaml(valid_yaml):
    CitationSchema(strict=True).load(valid_yaml)
