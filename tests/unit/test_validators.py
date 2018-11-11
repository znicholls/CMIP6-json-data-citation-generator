def test_load_template_yaml(valid_yaml):
    CitationSchema(strict=True).load(valid_yaml)
