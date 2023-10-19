from kafka import KafkaProducer
import csv

#Kafka producer settings
bootstrap_servers = 'localhost:9092'
topic_name = 'toll'

#Start Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

#CSV file Path
csv_file_path = '/home/project/kafka_2.12-2.8.0/transformed_data.csv'

#Sends data to the Kafka topic
with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        producer.send(topic_name, ','.join(row).encode('utf-8'))

print('File uploaded to Kafka topic')
