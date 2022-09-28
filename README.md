Requirements:
- docker: https://docs.docker.com/desktop/install/windows-install/
- docker-compose: https://docs.docker.com/desktop/install/windows-install/


Steps:

1. pip install -r requirements.txt
2. mkdir -p ./dags ./logs ./plugins
3. echo -e "AIRFLOW_UID=$(id -u)" > .env
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