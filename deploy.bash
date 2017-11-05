#!/bin/bash -e

cat <<EOF >> ~/.pypirc
[distutils]
index-servers=pypi
[pypi]
repository=https://upload.pypi.org/pypi
username=${PYPI_USERNAME}
password=${PYPI_PASSWORD}
EOF
python setup.py sdist upload;
rm ~/.pypirc;
