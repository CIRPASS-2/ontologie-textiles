#!/usr/bin/env bash

pip install -r requirements.txt

python3 unece-202209-v1.2.py --fhtml unece-202209-v1.2-tidy.htm --out unece-202209-v1.2.json

echo 'done...'