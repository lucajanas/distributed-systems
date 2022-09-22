Requirements:
- docker: https://docs.docker.com/desktop/install/windows-install/
- docker-compose: https://docs.docker.com/desktop/install/windows-install/


Steps:

1. mkdir -p ./dags ./logs ./plugins
2. echo -e "AIRFLOW_UID=$(id -u)" > .env
3. docker-compose up airflow-init
4. docker-compose up -d
5. wait till containers are up and running

UIs:
- Airflow:
   - url:      localhost:8080
   - user:     airflow
   - password: airflow
- Spark:
   - url:      localhost:9000
