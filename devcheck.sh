#!/bin/bash
set -x
python setup.py test || exit
prospector peyutil || exit
cd doc || exit 
make html || exit
cd -
