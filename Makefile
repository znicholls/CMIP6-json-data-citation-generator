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
		./venv/bin/black --exclude _version.py --py36 setup.py src tests docs/conf.py; \
	else \
		echo Not trying any formatting. Working directory is dirty ... >&2; \
	fi;

# first time setup, follow this https://blog.jetbrains.com/pycharm/2017/05/how-to-publish-your-package-on-pypi/
# then this works
.PHONY: publish-on-testpypi
publish-on-testpypi:
	-rm -rf build dist
	@status=$$(git status --porcelain); \
	if test "x$${status}" = x; then \
		$(call activate_conda_env,); \
			python setup.py sdist bdist_wheel --universal; \
			twine upload -r testpypi dist/*; \
	else \
		echo Working directory is dirty >&2; \
	fi;

test-testpypi-install: venv
	$(eval TEMPVENV := $(shell mktemp -d))
	python3 -m venv $(TEMPVENV)
	$(TEMPVENV)/bin/pip install pip --upgrade
	# Install dependencies not on testpypi registry
	$(TEMPVENV)/bin/pip install pandas
	# Install pymagicc without dependencies.
	$(TEMPVENV)/bin/pip install \
		-i https://testpypi.python.org/pypi netcdf-scm \
		--no-dependencies --pre
	@echo "This doesn't test dependencies"
	$(TEMPVENV)/bin/python -c "from netcdf_scm import *; import cmip6_data_citation_generator; print(cmip6_data_citation_generator.__version__)"

.PHONY: publish-on-pypi
publish-on-pypi:
	-rm -rf build dist
	@status=$$(git status --porcelain); \
	if test "x$${status}" = x; then \
		$(call activate_conda_env,); \
			python setup.py sdist bdist_wheel --universal; \
			twine upload dist/*; \
	else \
		echo Working directory is dirty >&2; \
	fi;

test-pypi-install: venv
	$(eval TEMPVENV := $(shell mktemp -d))
	python3 -m venv $(TEMPVENV)
	$(TEMPVENV)/bin/pip install pip --upgrade
	$(TEMPVENV)/bin/pip install netcdf_scm --pre
	$(TEMPVENV)/bin/python scripts/test_install.py

.PHONY: test-install
test-install: venv
	$(eval TEMPVENV := $(shell mktemp -d))
	python3 -m venv $(TEMPVENV)
	$(TEMPVENV)/bin/pip install pip --upgrade
	$(TEMPVENV)/bin/pip install .
	$(TEMPVENV)/bin/python scripts/test_install.py

clean:
	rm -rf venv

.PHONY: clean test black flake8 docs publish-on-pypi test-pypi-install
