#!/bin/bash

start-master.sh --ip 172.18.0.22
start-worker.sh spark://172.18.0.22:7077
jupyter-lab --no-browser --allow-root --ip=172.18.0.22 --NotebookApp.token='' --NotebookApp.password=''