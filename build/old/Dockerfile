FROM openjdk:8-alpine
RUN apk --update add wget tar bash
RUN wget http://mirrors.advancedhosters.com/apache/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz
RUN tar -xzf spark-3.3.1-bin-hadoop3.tgz && mv spark-3.3.1-bin-hadoop3 /spark && rm spark-3.3.1-bin-hadoop3.tgz
COPY start-master.sh /start-master.sh
COPY start-worker.sh /start-worker.sh