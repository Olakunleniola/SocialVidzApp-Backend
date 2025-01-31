#!/bin/bash

pip install -r requirements.txt

gunicorn -w 4 -k uvicorn.workers.UvicornWorker --timeout 120 --access-logfile - app.main:app