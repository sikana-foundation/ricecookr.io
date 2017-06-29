#!/usr/bin/python

import os
import yaml

# Reading API credentials from parameters.yml
with open("parameters.yml", "r") as f:
    parameters = yaml.load(f)

# Sikana's API access
KOLIBRI_TOKEN = parameters["kolibri"]["token"]
LANGUAGES = ["en", "fr", "es", "pt", "pt-br", "pl", "tr", "ru", "zh", "zh-tw"]

for ln in LANGUAGES:
    os.system("python3 -m ricecooker uploadchannel \"ricecookr.py\" --publish --token={} language_code={}".format(KOLIBRI_TOKEN, ln))
