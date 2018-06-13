SHELL=/bin/bash
ROOT_DIR=$(shell pwd)

DEV_REQUIREMENTS=$(ROOT_DIR)/dev-requirements.txt
VIRTUAL_ENV_DIR=$(ROOT_DIR)/venv

define activate_venv
	source $(VIRTUAL_ENV_DIR)/bin/activate
endef

.PHONY : make_venv
make_venv : $(VIRTUAL_ENV_DIR)
$(VIRTUAL_ENV_DIR) : $(DEV_REQUIREMENTS)
	python -m venv venv
	( \
		$(call activate_venv,); \
		which python; \
		pip install --upgrade pip; \
		pip install -Ur dev-requirements.txt \
	)

.PHONY : variables
variables :
	@echo SHELL: $(SHELL)
	@echo ROOT_DIR: $(ROOT_DIR)

	@echo DEV_REQUIREMENTS: $(DEV_REQUIREMENTS)
	@echo VIRTUAL_ENV_DIR: $(VIRTUAL_ENV_DIR)
