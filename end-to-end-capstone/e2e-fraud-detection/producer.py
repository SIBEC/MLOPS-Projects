import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer
from faker import Faker

fake = Faker()


def generate_transaction():
    """Generates a single fake credit card transaction."""
    # Simulate a small percentage of transactions as fraudulent
    is_fraud = random.choice([True, False, False, False, False])  # Approx 20% fraud rate

    # Fraudulent transactions tend to be for larger amounts
    amount = round(random.uniform(500, 2000) if is_fraud else random.uniform(1, 500), 2)

    return {
        "transaction_id": fake.uuid4(),
        "user_id": fake.uuid4(),
        "amount": amount,
        "timestamp": datetime.now().isoformat(),
        "merchant_id": fake.uuid4(),
        "is_fraud": is_fraud
    }


def serializer(message):
    """JSON serializer for Kafka messages."""
    return json.dumps(message).encode('utf-8')


if __name__ == "__main__":
    # Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=serializer
    )

    print("Starting to produce transactions...")
    try:
        while True:
            # Generate a new transaction
            transaction = generate_transaction()

            # Send it to the 'transactions' topic
            producer.send('transactions', transaction)

            print(
                f"Produced transaction: {transaction['transaction_id']} | Amount: ${transaction['amount']:.2f} | Fraud: {transaction['is_fraud']}")

            # Wait for a short period before sending the next one
            time.sleep(random.uniform(0.5, 2.0))

    except KeyboardInterrupt:
        print("\nStopping producer.")
    finally:
        producer.close()
