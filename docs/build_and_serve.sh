#!/bin/bash

# Build docs
PYTHONPATH=. pydoc-markdown

# Serve docs
mkdocs serve -f ./build/docs/mkdocs.yml
