from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
import random
import time
import datetime


# Function to generate random IoT data
def generate_iot_data(**kwargs):
    data = []
    for _ in range(60):  # 60 readings (1 per second) over one minute
        data.append(random.choice([0, 1]))
        time.sleep(1)  # simulate a 1-second interval
    return data


# Function to aggregate the IoT data
def aggregate_machine_data(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='getting_iot_data')
    count_0 = data.count(0)
    count_1 = data.count(1)
    aggregated_data = {'count_0': count_0, 'count_1': count_1}
    return aggregated_data


# # Email content generation
# def create_email_content(**kwargs):
#     ti = kwargs['ti']
#     aggregated_data = ti.xcom_pull(task_ids='aggregate_machine_data')
#     return (f"Aggregated IoT Data:\n"
#             f"Count of 0: {aggregated_data['count_0']}\n"
#             f"Count of 1: {aggregated_data['count_1']}")


# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}


with DAG(
    dag_id='iot_data_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:


    start_task = DummyOperator(task_id='start_task')


    getting_iot_data = PythonOperator(
        task_id='getting_iot_data',
        python_callable=generate_iot_data,
    )


    aggregate_machine_data = PythonOperator(
        task_id='aggregate_machine_data',
        python_callable=aggregate_machine_data,
    )


    # # Optionally, use an EmailOperator to send the results
    # send_email = EmailOperator(
    #     task_id='send_email',
    #     to='technician@example.com',
    #     subject='IoT Data Aggregation Results',
    #     html_content=create_email_content(),
    # )


    end_task = DummyOperator(task_id='end_task')


    # Define the task dependencies
    start_task >> getting_iot_data >> aggregate_machine_data >> end_task