#!/bin/bash
echo 'running tests, then prospector (several python checking prereqs must be installed), and sphinx.'
set -x
python setup.py test || exit
prospector peyutil || exit
cd doc || exit 
make html || exit
cd -
