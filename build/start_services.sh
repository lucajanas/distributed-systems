#!/bin/bash

if [[ $MODE == "MASTER" ]]; then
  start-master.sh --ip 172.18.0.22;
  jupyter-lab --no-browser --allow-root --ip=172.18.0.22 --NotebookApp.token='' --NotebookApp.password=''
elif [[ $MODE == "WORKER" ]]; then
  start-worker.sh spark://172.18.0.22:7077;
  sleep infinity
else
  exit 1
fi