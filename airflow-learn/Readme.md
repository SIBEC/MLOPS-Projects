# Run following commands

curl https://airflow.apache.org/docs/apache-airflow/2.10.2/docker-compose.yaml > docker-compose.yaml
mkdir example-orchestration
mv docker-compose.yaml example-orchestration/
cd example-orchestration/
mkdir dags logs plugins config
export AIRFLOW_UID=$(id -u)
echo "AIRFLOW_UID=$(id -u)" > ~/example-orchestration/.env 

# Change Port
Change the airflow-webserver port in docker-compose.yaml to expose port 8080 on the host system at port 8081.

# Initialize Airflow
docker compose up airflow-init

# Start Airflow
docker compose up -d

# DAG

cd dags/
vim iot_dag.py
