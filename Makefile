APP_NAME = $(shell python setup.py --name)
VENV_PREFIX = $(shell echo $(APP_NAME) | tr [a-z] [A-Z])
VENV_NAME = py36-$(APP_NAME)
VERSION = $(shell python setup.py --version)
ENV = dev


PIP = $(WORKON_HOME)/$(VENV_NAME)/bin/pip3
PYTHON = $(WORKON_HOME)/$(VENV_NAME)/bin/python3
VIRTUALENV = $(PYENV_ROOT)/versions/3.6.0/bin/virtualenv


LINT_OPTION = --max-line-length 180 --ignore _ --import-order-style=edited --application-import-names=common,config,scripts,tests,utils --exclude=vendors/


init: init-venv update-venv init-runtime


init-dev: init
	$(PIP) install -Ur requirements-dev.txt
	touch config/settings_dev.yaml


init-venv:
	test -d $(WORKON_HOME)/$(VENV_NAME) || $(VIRTUALENV) $(WORKON_HOME)/$(VENV_NAME)


init-runtime:  ## Initialize application vendors dependencies
	mkdir -p vendors && $(PIP) install -t vendors -Ur requirements.txt


build:  init-runtime ## Build an application package suitable for distribution
	echo $(VERSION) > VERSION
	echo $(VERSION) > latest
	test -e dist/$(APP_NAME)-$(VERSION).tar.gz || ($(PYTHON) setup.py sdist)


update-venv:
	$(PIP) install -U pip


get-artifact-name:  ## Return the build artifact filename
	echo $(APP_NAME)-$(VERSION).tar.gz

deinit:
	rm -rf $(WORKON_HOME)/$(VENV_NAME)


lint:
	$(WORKON_HOME)/$(VENV_NAME)/bin/flake8 $(LINT_OPTION) .


test: lint
	PYTHONPATH=.:vendors $(VENV_PREFIX)_SETTINGS=config/settings_test.yaml $(WORKON_HOME)/$(VENV_NAME)/bin/py.test tests


test-debug: lint
	PYTHONPATH=.:vendors $(VENV_PREFIX)_SETTINGS=config/settings_test.yaml $(WORKON_HOME)/$(VENV_NAME)/bin/py.test --ipdb tests


assets:
	true || true


coverage: lint
	PYTHONPATH=.:vendors $(VENV_PREFIX)_SETTINGS=config/settings_test.yaml $(WORKON_HOME)/$(VENV_NAME)/bin/py.test --cov . --cov-report term-missing --cov-report xml --junitxml=junit-coverage.xml --cov-config .coveragerc tests


clean:
	true || true


help: ## Show this help.
	@grep -E "^[^.][a-zA-Z_-]*:" Makefile | awk -F '[:#]' '{print $$1, ":", $$NF}' | sort | column -t -s:


.SILENT: deinit init init-venv init-runtime update-venv init-dev -prod build distribute run lint test test-debug coverage clean get-artifact-name get-gs-app-path build
.PHONY: deinit init init-venv init-runtime update-venv init-dev -prod build distribute run lint test test-debug coverage clean get-artifact-name get-gs-app-path build
