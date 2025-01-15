#!/bin/bash

pip install requirements.txt

gunicorn -w -4 -k uvicorn.workers.UvicornWorker app.main:app
