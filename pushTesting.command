#! /bin/bash


cd ~/Desktop/Data_Sense/senior_project
python3.7 backendTesting.py || { echo 'Backend Testing Failed' ; exit 1; }
python3.7 frontend-testing.py || { echo 'Frontend Testing Failed' ; exit 1;}
git add .
git commit -m "Auto Tested Update"
git push origin master
