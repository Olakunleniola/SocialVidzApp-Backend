#!/bin/bash

pip install requirement.txt

gunicorn -w -4 -k uvicorn.workers.UvicornWorker app.main:app
