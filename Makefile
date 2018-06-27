SHELL=/bin/bash
ROOT_DIR=$(shell pwd)

SETUP_PY=$(ROOT_DIR)/setup.py
VIRTUAL_ENV_DIR=$(ROOT_DIR)/venv

VIRTUAL_ENV_DIR_PY2=$(ROOT_DIR)/venv2

EXAMPLE_ROOT_DIR=$(ROOT_DIR)/examples
EXAMPLE_FILE_DIR=$(EXAMPLE_ROOT_DIR)/data/empty-test-files/
EXAMPLE_YML=$(EXAMPLE_ROOT_DIR)/yaml-templates/yaml-example.yml
MAKE_JSON_COMMAND=$(ROOT_DIR)/scripts/generate_CMIP6_json_files.py
EXAMPLE_OUTPUT_DIR=$(EXAMPLE_ROOT_DIR)/outputs

.PHONY : make_example_jsons
make_example_jsons : $(VIRTUAL_ENV_DIR) $(EXAMPLE_FILE_DIR) $(EXAMPLE_YML)
	$(call activate_venv,); $(MAKE_JSON_COMMAND) $(EXAMPLE_YML) $(EXAMPLE_FILE_DIR) $(EXAMPLE_OUTPUT_DIR)

.PHONY : test
test : $(VIRTUAL_ENV_DIR) $(VIRTUAL_ENV_DIR_PY2)
	$(call activate_venv,); pytest --cov
	$(call activate_venv2,); pytest --cov

define activate_venv
	source $(VIRTUAL_ENV_DIR)/bin/activate
endef

define activate_venv2
	source $(VIRTUAL_ENV_DIR_PY2)/bin/activate
endef

.PHONY : remove_venvs
remove_venvs :
	rm -rf $(VIRTUAL_ENV_DIR) $(VIRTUAL_ENV_DIR_PY2)

.PHONY : make_venvs
make_venvs : $(VIRTUAL_ENV_DIR) $(VIRTUAL_ENV_DIR_PY2)
.PHONY : make_venv
make_venv : $(VIRTUAL_ENV_DIR)
$(VIRTUAL_ENV_DIR) : $(SETUP_PY)
	python3 -m venv $(VIRTUAL_ENV_DIR)
	( \
		$(call activate_venv,); \
		which python; \
		python --version; \
		pip install --upgrade pip; \
		python $(SETUP_PY) develop \
	)
	touch $(VIRTUAL_ENV_DIR)

.PHONY : make_venv2
make_venv : $(VIRTUAL_ENV_DIR_PY2)
$(VIRTUAL_ENV_DIR_PY2) : $(SETUP_PY)
	pip install virtualenv
	python2 -m virtualenv $(VIRTUAL_ENV_DIR_PY2)
	( \
		$(call activate_venv2,); \
		which python; \
		python --version; \
		pip install --upgrade pip; \
		python $(SETUP_PY) develop \
	)
	touch $(VIRTUAL_ENV_DIR_PY2)

.PHONY : clean
clean :
	make remove_venvs


.PHONY : variables
variables :
	@echo SHELL: $(SHELL)
	@echo ROOT_DIR: $(ROOT_DIR)

	@echo SETUP_PY: $(SETUP_PY)
	@echo VIRTUAL_ENV_DIR: $(VIRTUAL_ENV_DIR)

	@echo VIRTUAL_ENV_DIR_PY2: $(VIRTUAL_ENV_DIR_PY2)

	@echo EXAMPLE_ROOT_DIR: $(EXAMPLE_ROOT_DIR)
	@echo EXAMPLE_FILE_DIR: $(EXAMPLE_FILE_DIR)
	@echo EXAMPLE_YML: $(EXAMPLE_YML)
	@echo MAKE_JSON_COMMAND: $(MAKE_JSON_COMMAND)
	@echo EXAMPLE_OUTPUT_DIR: $(EXAMPLE_OUTPUT_DIR)
