# Start from the official Airflow image
FROM apache/airflow:2.8.1

# Switch to root to grant permissions, then back to airflow user
USER root
RUN chown -R airflow:root /opt/airflow/
USER airflow

# Copy the requirements file
COPY requirements.txt /

# Install the python packages
RUN pip install --no-cache-dir --user -r /requirements.txt
