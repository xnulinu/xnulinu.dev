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

# no-store headers: the preview always shows the latest build, never a cached page or stylesheet
serve:
	python3 -c "import http.server as s; H = type('H', (s.SimpleHTTPRequestHandler,), {'end_headers': lambda self: (self.send_header('Cache-Control', 'no-store'), s.SimpleHTTPRequestHandler.end_headers(self))}); s.ThreadingHTTPServer(('', 8000), H).serve_forever()"

clean:
	rm -rf $(VENV)
