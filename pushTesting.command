#! /bin/bash


cd ~/Desktop/Data_Sense/senior_project
python3.7 backendTesting.py || { echo 'Backend Testing Failed' ; exit 1; }
git add .
git commit -m "Auto Update"
git push origin master
