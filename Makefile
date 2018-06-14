SHELL=/bin/bash
ROOT_DIR=$(shell pwd)

DEV_REQUIREMENTS=$(ROOT_DIR)/dev-requirements.txt
SETUP_PY=$(ROOT_DIR)/setup.py
VIRTUAL_ENV_DIR=$(ROOT_DIR)/venv

VIRTUAL_ENV_DIR_PY2=$(ROOT_DIR)/venv2

@echo VIRTUAL_ENV_DIR_PY2: $(VIRTUAL_ENV_DIR_PY2)

.PHONY : test
test : $(VIRTUAL_ENV_DIR) $(VIRTUAL_ENV_DIR_PY2)
	$(call activate_venv,); pytest
	$(call activate_venv2,); pytest

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
$(VIRTUAL_ENV_DIR) : $(DEV_REQUIREMENTS) $(SETUP_PY)
	python3 -m venv $(VIRTUAL_ENV_DIR)
	( \
		$(call activate_venv,); \
		which python; \
		python --version; \
		pip install --upgrade pip; \
		pip install -Ur dev-requirements.txt; \
		python $(SETUP_PY) develop \
	)
	touch $(VIRTUAL_ENV_DIR)

$(VIRTUAL_ENV_DIR_PY2) : $(DEV_REQUIREMENTS) $(SETUP_PY)
	pip install virtualenv
	python2 -m virtualenv $(VIRTUAL_ENV_DIR_PY2)
	( \
		$(call activate_venv2,); \
		which python; \
		python --version; \
		pip install --upgrade pip; \
		pip install -Ur dev-requirements.txt; \
		python $(SETUP_PY) develop \
	)
	touch $(VIRTUAL_ENV_DIR_PY2)

.PHONY : variables
variables :
	@echo SHELL: $(SHELL)
	@echo ROOT_DIR: $(ROOT_DIR)

	@echo DEV_REQUIREMENTS: $(DEV_REQUIREMENTS)
	@echo SETUP_PY: $(SETUP_PY)
	@echo VIRTUAL_ENV_DIR: $(VIRTUAL_ENV_DIR)
