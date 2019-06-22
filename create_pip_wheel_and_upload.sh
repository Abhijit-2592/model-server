#!/bin/bash
bash ./compile_protobufs.sh
echo "Creating pip wheel!"
python3 setup.py sdist bdist_wheel
echo "Wheel created"
# make sure you have ~/.pypirc file
echo "uploading to pypip server"
python3 -m twine upload --verbose --repository-url https://upload.pypi.org/legacy/ dist/*
