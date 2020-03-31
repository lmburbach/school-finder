#! /bin/bash

sudo apt-get install python3.7-venv
python3.7 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
deactivate