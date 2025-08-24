import json
import pandas as pd
from kafka import KafkaConsumer
import os

# The path for our data log file
DATA_FILE = 'data/transactions_log.csv'


def initialize_data_file():
    """Creates the CSV file with headers if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=['transaction_id', 'user_id', 'amount', 'timestamp', 'merchant_id', 'is_fraud'])
        df.to_csv(DATA_FILE, index=False)
        print(f"Created data file: {DATA_FILE}")


if __name__ == "__main__":
    # Ensure the data directory and file exist
    os.makedirs('data', exist_ok=True)
    initialize_data_file()

    # Kafka Consumer
    consumer = KafkaConsumer(
        'transactions',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',  # Start reading at the earliest message
        group_id='fraud-detector-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print("Starting to consume transactions and log them...")
    try:
        for message in consumer:
            # The message value is the transaction dictionary
            transaction_data = message.value

            # Append the new transaction to our CSV log
            df = pd.DataFrame([transaction_data])
            df.to_csv(DATA_FILE, mode='a', header=False, index=False)

            print(f"Logged transaction: {transaction_data['transaction_id']}")

    except KeyboardInterrupt:
        print("\nStopping consumer.")
    finally:
        consumer.close()