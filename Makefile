# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SPHINXAPIDOC  ?= sphinx-apidoc
SOURCEDIR     = docsource
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Lint our codebase
lint:
	isort --atomic --apply --recursive ori tests
	black .
	pylint ori tests
	mypy ori tests

tox:
	docker-compose run tox

test:
	python -m unittest

# Update dependencies and sync with our dependencies.
# We need the .requirements.txt file because readthedocs.io does not support
# poetry yet.
updatedeps:
	poetry update
	poetry export --dev --format requirements.txt > .requirements.txt

.PHONY: help lint tox test Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
