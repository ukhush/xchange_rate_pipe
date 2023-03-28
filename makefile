VENV = crud_ops_env
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
GOOGLE_CRED_FILE= '/Users/umairk/Downloads/ukhushn-proj2-kkey.json'

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt


run: $(VENV)/bin/activate
	$(PYTHON) unit_test.py --google_cred_path $(GOOGLE_CRED_FILE)



