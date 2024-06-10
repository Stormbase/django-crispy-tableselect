# Script to install dependencies in a tox environment

hatch dep show requirements | pip install -r /dev/stdin
pip install -e . $@