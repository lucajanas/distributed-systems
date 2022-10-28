FROM ubuntu:latest

USER root:root

RUN apt update
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
RUN DEBIAN_FRONTEND=noninteractive apt install -y software-properties-common
RUN apt install -y net-tools curl wget

RUN apt install -y python3-pip
RUN apt install -y default-jdk
RUN pip install pyspark

WORKDIR /tmp
ADD https://downloads.apache.org/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz ./
RUN tar -xf spark-3.3.1-bin-hadoop3.tgz \
    && mv spark-3.3.1-bin-hadoop3 /opt/spark
ENV PATH="${PATH}:/opt/spark/sbin"
ENV SPARK_HOME="/opt/spark"
ENV PYSPARK_PYTHON="/usr/bin/python3"

RUN pip install jupyterlab

COPY start_services.sh /opt

EXPOSE 8080
EXPOSE 7077
EXPOSE 8081
EXPOSE 8888

ENTRYPOINT ["/opt/start_services.sh"]