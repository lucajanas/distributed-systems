#!/bin/bash

NETWORK_NAME=spark-network
SUBNET=172.18.0.0/16
IP=172.18.0.22

if [ -z $(docker network ls --filter name=^${NETWORK_NAME}$ --format="{{ .Name }}") ] ; then
    docker network create --subnet=${SUBNET} ${NETWORK_NAME};
    echo "Created network $NETWORK_NAME" 
fi

docker run -v $PWD/load_simulation_data://data:rw --net spark-network --ip ${IP} --rm --name spark -d -e MODE="MASTER" -p 8080:8080 -p 7077:7077 -p 8081:8081 -p 8888:8888 lucajanas/spark
docker run -v $PWD/load_simulation_data://data:rw --net spark-network --rm --name spark-worker-1 -e MODE="WORKER" -d lucajanas/spark
docker run -v $PWD/load_simulation_data://data:rw --net spark-network --rm --name spark-worker-2 -e MODE="WORKER" -d lucajanas/spark
echo "Started container"
