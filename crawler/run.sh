#!/bin/bash 

# Activate Env
ENV_PATH=/Users/nasa56_mini/workspace/pricewatcher/env/pricewatcher/bin/activate
source ${ENV_PATH}

RUN_DIR=/Users/nasa56_mini/workspace/pricewatcher/Server/crawler/
cd ${RUN_DIR}

# Start Crawler
pw-run-crawlers --output-dir /Users/nasa56_mini/DATA
