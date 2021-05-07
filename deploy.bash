#!/bin/bash -e

cat <<EOF >> ~/.pypirc
[distutils]
index-servers=pypi
[pypi]
repository=https://upload.pypi.org/legacy/
username=${PYPI_USERNAME}
password=${PYPI_PASSWORD}
EOF
python setup.py sdist bdist_wheel;
twine upload dist/*;
rm ~/.pypirc;