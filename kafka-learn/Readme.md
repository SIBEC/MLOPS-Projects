# Install Kafka
pip3 install kafka-python kafka-python-ng

# Create Topic
docker exec <container_name> kafka-topics \
  --create \
  --topic sample-topic \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

# Create Producer and Consumer