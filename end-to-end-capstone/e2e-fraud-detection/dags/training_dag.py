# filename: dags/training_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

# Define file paths relative to the Airflow container
DATA_PATH = '/opt/airflow/data/transactions_log.csv'
MODEL_PATH = '/opt/airflow/models/fraud_model.pkl'


def train_model_task():
    """
    Reads transaction data, trains a logistic regression model,
    and saves it to a file.
    """
    print("Starting model training task...")

    # Ensure model directory exists
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    # Check if data file exists and is not empty
    if not os.path.exists(DATA_PATH) or os.path.getsize(DATA_PATH) == 0:
        print("Data file not found or is empty. Skipping training.")
        return

    # Load data
    df = pd.read_csv(DATA_PATH)

    if df.shape[0] < 10:
        print(f"Not enough data to train. Found only {df.shape[0]} records. Skipping.")
        return

    print(f"Loaded {df.shape[0]} records for training.")

    # For simplicity, we'll only use 'amount' as a feature.
    # In a real project, you would do extensive feature engineering here.
    features = ['amount']
    target = 'is_fraud'

    X = df[features]
    y = df[target]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Train model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model trained successfully. Test Accuracy: {acc:.4f}")

    # Save the trained model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
        'fraud_detection_model_training',
        default_args=default_args,
        description='A DAG to train a fraud detection model daily',
        schedule_interval='@daily',  # Run once a day
        catchup=False,
) as dag:
    # Define the PythonOperator
    train_task = PythonOperator(
        task_id='train_fraud_detection_model',
        python_callable=train_model_task,
    )

