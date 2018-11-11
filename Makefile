venv: setup.py
	[ -d ./venv ] || python3 -m venv ./venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install versioneer
	./venv/bin/pip install -e .[test,docs,deploy]
	touch venv

test: venv
	./venv/bin/pytest --cov -rfsxEX --cov-report term-missing

docs: venv
	./venv/bin/sphinx-build -M html docs docs/_build

flake8: venv
	./venv/bin/flake8 src tests setup.py _version.py

.PHONY: black
black: venv
	@status=$$(git status --porcelain pymagicc tests); \
	if test "x$${status}" = x; then \
		./venv3/bin/black --exclude _version.py --py36 setup.py src tests docs/conf.py; \
	else \
		echo Not trying any formatting. Working directory is dirty ... >&2; \
	fi;

publish-on-pypi: venv
	-rm -rf build dist
	@status=$$(git status --porcelain); \
	if test "x$${status}" = x; then \
		./venv/bin/python setup.py bdist_wheel --universal; \
		./venv/bin/twine upload dist/*; \
	else \
		echo Working directory is dirty >&2; \
	fi;

test-pypi-install: venv
	$(eval TEMPVENV := $(shell mktemp -d))
	python3 -m venv $(TEMPVENV)
	$(TEMPVENV)/bin/pip install pip --upgrade
	$(TEMPVENV)/bin/pip install cmip6_data_citation_generator
	$(TEMPVENV)/bin/python -c "import sys; sys.path.remove(''); import cmip6_data_citation_generator; print(cmip6_data_citation_generator.__version__)"

clean:
	rm -rf venv

.PHONY: clean test black flake8 docs publish-on-pypi test-pypi-install
