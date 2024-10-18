#!/bin/sh

sudo apt install python3.8
sudo apt install python3.8-venv

python3.8 --version
python3.8 -m pip install --upgrade pip
python3.8 -m pip install --upgrade build

rm -rf dist
mkdir dist
rm -rf .gitignore

python3.8 -m build
git reset --hard

python3.8 -m pip install --upgrade twine
# python3.8 -m twine upload --repository testpypi dist/*
python3.8 -m twine upload dist/* --verbose --repository cochl-sense-api

# python3.8 -c 'import cochl.sense; print(cochl.sense.APIConfig())'
