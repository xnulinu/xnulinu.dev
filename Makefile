# xnulinu.dev — site tasks
#
#   make blog    build the blog (posts/*.md -> html)
#   make serve   preview the whole site at http://localhost:8000
#   make clean   remove the build virtualenv

VENV := .venv
PY   := $(VENV)/bin/python
PIP  := $(VENV)/bin/pip

.PHONY: blog serve clean

blog: $(VENV)
	$(PY) blog/build.py

# create an isolated venv with the one dependency (system Python is externally managed)
$(VENV):
	python3 -m venv $(VENV)
	$(PIP) install --quiet --upgrade pip
	$(PIP) install --quiet markdown

serve:
	python3 -m http.server 8000

clean:
	rm -rf $(VENV)
