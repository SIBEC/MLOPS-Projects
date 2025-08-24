# Setup Project

Directory Structure

e2e-fraud-detection/
├── data/                 # To store our transaction log
├── models/               # To store the trained model
├── dags/                 # For Airflow DAG files
│   └── training_dag.py
├── .env                  # Environment variables for Docker
├── docker-compose.yml    # To run Kafka & Airflow
├── producer.py           # Kafka producer script
├── consumer.py           # Kafka consumer script
├── service.py            # BentoML service definition
└── bentofile.yaml        # BentoML configuration
- Dockerfile
- requirements.txt

`
mkdir -p e2e-fraud-detection/data e2e-fraud-detection/models e2e-fraud-detection/dags && \
cd e2e-fraud-detection && \
touch dags/training_dag.py .env docker-compose.yml producer.py consumer.py service.py bentofile.yaml requirements.txt Dockerfile
`

## 2. Python Dependencies:

Make sure you have Python installed, then install the required libraries:

`pip install kafka-python pandas scikit-learn bentoml faker`
## You will also need airflow, but we will run it in Docker.

3. Docker Configuration (docker-compose.yml and .env):

This docker-compose.yml file will set up Zookeeper, Kafka, and a complete Airflow environment.
Add the UID In the .env file:

`AIRFLOW_UID=50000`

export AIRFLOW_UID=$(id -u)
docker-compose up -d

# How to Run Everything

Start Services: Open a terminal in your project directory and run:
```
docker-compose up -d
```

Start the Producer: Open a new terminal and run the producer. It will start generating data.
```
python producer.py
```
Start the Consumer: Open a third terminal and run the consumer. You will see it logging the data produced in the other terminal.
```
python consumer.py
```
Let this run for a few minutes to collect some data. You can check the data/transactions_log.csv file to see the records.

## Trigger the Airflow DAG:

Open your web browser and go to http://localhost:8081.

You will see the fraud_detection_model_training DAG.

Enable the DAG by clicking the toggle on the left.

To run it immediately, click the "play" button on the right.

You can click on the DAG name and then "Graph" or "Grid" view to see the task running. Check the logs to see the training output and model accuracy. After it succeeds, a fraud_model.pkl file will appear in your models/ directory.

## Serve the Model with BentoML:

Write your bentofile.yaml then do 
```
bentoml build .
```

Make sure you have a trained model in the models/ folder.

First, let's import the model into BentoML's local store. This makes it versioned and manageable.

```
python - <<'PY'
import joblib, bentoml
model = joblib.load("models/fraud_model.pkl")   # path to your pickle
bentoml.sklearn.save_model("fraud_model", model)   # creates tag fraud_model:<timestamp>
PY
```

This will register the model. Note the tag it gives you (e.g., fraud_model:somehash). Your bentofile.yaml will automatically pick up the latest version.

Now, serve the API in development mode:
```
bentoml serve service.py:svc --reload
```

This will start a server, usually at http://127.0.0.1:3000.

# Test the Live API:

Open a fourth terminal and use curl to send a test transaction. Let's test a high-value transaction that is likely to be flagged as fraud.

`curl -X POST -H "Content-Type: application/json" --data "[[1500.50]]" http://127.0.0.1:3000/classify`

You should get a response like: {"predictions": true} (1 means fraud).

Now test a low-value transaction:

`curl -X POST -H "Content-Type: application/json" --data "[[25.20]]" http://127.0.0.1:3000/classify`

You should get a response like: {"predictions": False} (0 means not fraud).

Congratulations! You have successfully built and connected a full end-to-end machine learning pipeline.