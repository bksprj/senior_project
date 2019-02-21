#! /bin/bash

cd
cd Desktop
git clone https://github.com/bksprj/senior_project.git
cd senior_project
python3 -m venv data-sense
source data-sense/bin/activate
pip install -r "requirements.txt"

