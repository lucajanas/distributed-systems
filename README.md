Requirements:
- docker: https://docs.docker.com/desktop/install/windows-install/
- docker-compose: https://docs.docker.com/desktop/install/windows-install/


Steps:

1. pip install -r requirements.txt
2. mkdir -p ./dags ./logs ./plugins
3. echo -e "AIRFLOW_UID=$(id -u)" > .env (only on linux)
4. docker-compose up airflow-init
5. docker-compose up -d
6. wait till containers are up and running

UIs:
- Airflow:
   - url:      localhost:8080
   - user:     airflow
   - password: airflow
- Spark:
   - url:      localhost:9000

To be able to use Spark, you need to have Java installed on your machine.

For Windows:

1. Download Java from https://www.java.com/en/download/
2. Install Java
3. Go to 'Systemumgebungsvariablen bearbeiten - Umgebungsvariablen' and set a new system variable JAVA_HOME, e.g C:\Program Files\Java\jre1.8.0_341

On linux:

sudo apt-get update

sudo apt-get install openjdk-8-jdk

On mac:

brew cask install java

To test the connection to the running spark master, execute connect.py.

You can check if your application has been submitted via your browser on localhost:9000.


# Guiding questions

1. What are the central components in your system? Describe the architecture of the constructed information system, name the central software components in your solution, and describe their purpose.

Our system consists of one containerized spark master and two containerized spark workers, controlled by docker-compose running on a single machine. You can submit spark applications to this cluster / the spark master by creating a SparkContext using pyspark from your local machine. The spark master distributes the requests to a worker with enough available resources to handle the request from the client (your local machine). The tasks assigned to a spark worker are then handled / processed by an executor within the spark worker.

![image](https://user-images.githubusercontent.com/58073358/197608242-660a6ee2-cc12-442d-b6d3-68aa0a5e4964.png)

Source: https://spark.apache.org/docs/latest/cluster-overview.html

2. What is the analytical problem that you want to solve? Present an adequate formal definition of your problem and describe the process how you solve it using the prototypical implementation in your data pipeline.

3. How does your analytical approach work and what changed compared to a non distributed version of the algorithm? Describe the algorithm that you chose to derive a solution with a focus on the tradeoffs that have been made in the distributed environment.

4. How can your solution be evaluated? Discuss how the quality of your analytical solution can be evaluated and present some evaluation statistics as results. The actual quality of your forecasts or classification is not of interest, but the process on how to derive evaluation statistics and how one would benchmark multiple models.

5. What are the limitations of your solution? Kleppmann (2017) mentions reliability, scalability, and maintainability as key success factors for distributed data intensive systems. How are those goals achieved in your system? What are the most relevant topics (e.g. sections or subsections from Kleppmanns book) when scaling your prototypical system?

Our docker-compose setup is neither highly available nor scalable or very maintainable as it is intended more as a prototype / testing environment. The containers controlled by docker-compose still run on a single machine, which leads to complete unavailability of the service in case this single machine fails, e. g. due to hardware failure. We have redundant spark workers, so if one of these workers fails due to internal problems, there still should be a backup worker which the master can forward requests to. We do not have a redundant spark master. In case of failure of the spark master, the complete service is not available. In order to reduce the risk of human errors, spark offers clients in many different languages such as Python, Java, Spark and R which offer abstracted functions to submit spark applications.

The scalability of our system is limited by the resources available on the local machine which runs the containers. Nevertheless, more spark workers can be added to the system by adjusting the docker-compose.yml until the resources of the local machine are used up.

The disadvantages and weaknesses of our system in regards to reliability and scalability could be dealt with by running spark in a kubernetes cluster with multiple physical nodes / virtual machines in it. Hereby, there could be redundant master and worker nodes in kubernetes which can handle the workload even in case one or more machine fails. With multiple machines in the kubernetes cluster, the scalability of the system would not be limited to the resources of a single machine. In addition, more nodes can be added to the kubernetes cluster quite easily to increase the available resources in case the cluster resources are exhausted. This addition (and possibly removing) of nodes can even happen dynamically depending on the resource utilization of the cluster. Hereby, temporary load peaks could be handled.

Regarding maintailability, updating the spark version is fairly easy. You just have to update the version of the spark container in the docker-compose.yml. But changing something in this setup requires a restart and therefore a downtime of the application. Here, too, kubernetes could possibly help by introducing rolling updates of the service. With rolling updates, kubernetes pods with the new spark version could be rolled out while the pods with the old version keep serving clients until the new spark version takes over.

Nevertheless, using the containerized version of spark removes a part of the complexity even in our docker-compose setup as the container images bring everything spark needs and can be tested as a whole. To improve the maintainability of our system, monitoring - e. g. using prometheus and grafana - would be very helpful.
