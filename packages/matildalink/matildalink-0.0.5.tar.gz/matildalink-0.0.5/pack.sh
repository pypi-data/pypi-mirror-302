#!/bin/sh

# Install required packages.
python3 -m pip install --upgrade pip build twine

# Generate distribution archives.
python3 -m build

# Upload the distribution archives.
#python3 -m twine upload --repository testpypi dist/* --verbose
python3 -m twine upload dist/* --verbose
