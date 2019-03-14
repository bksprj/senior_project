#! /bin/bash

cd
pip install -U selenium
cd Desktop
mkdir Data_Sense
cd Data_Sense
git clone https://github.com/bksprj/senior_project.git
python3 -m venv data_sense
source data_sense/bin/activate
pip install -r "senior_project/requirements.txt"
deactivate
