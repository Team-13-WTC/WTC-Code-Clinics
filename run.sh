#!/bin/bash

if [[ ! -d "env" ]]
then
    python3 -m venv .
fi

source run
pip3 --disable-pip-version-check  install -r requirements.txt > install_log.txt
#if you want to run program, do it here
python3 user.py
deactivate