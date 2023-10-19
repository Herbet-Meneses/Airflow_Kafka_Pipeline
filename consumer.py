from datetime import datetime
from kafka import KafkaConsumer
import mysql.connector

#Settings
topic_name = 'toll'
db_host = 'localhost'
db_user = 'root'
db_password = 'MTA0NTctZmhtZW5l'
db_database = 'tolldata'

#Connecting to MySQL
print("Connecting to the database")
try:
    db_connection = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_database)
except Exception:
    print("Could not connect to database. Check credentials")
else:
    print("Connected to database")
db_cursor = db_connection.cursor()

#Connecting to Kafka
print("Connecting to Kafka")
consumer = KafkaConsumer(topic_name, bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
print("Connected to Kafka")
print(f"Reading messages from the topic {topic_name}")

#Extract, transform and load data from Kafka into the database
for msg in consumer:

    try:
        print('Extract information from kafka')
        message = msg.value.decode("utf-8")
        
        print('Transform the date format to suit the database schema')
        (Row_id, Timestamp, Anonymized_Vehicle_number, Vehicle_type, Number_of_axles, Tollplaza_id, Tollplaza_code, Type_of_Payment_code, Vehicle_Code) = message.split(",")

        dateobj = datetime.strptime(Timestamp, '%a %b %d %H:%M:%S %Y')
        Timestamp = dateobj.strftime("%Y-%m-%d %H:%M:%S")
        
        print('Loading data into the database table')
        sql = "insert into livetolldata values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result = db_cursor.execute(sql, (Row_id, Timestamp, Anonymized_Vehicle_number, Vehicle_type, Number_of_axles, Tollplaza_id, Tollplaza_code, Type_of_Payment_code, Vehicle_Code))
        print(f"A {Vehicle_type} was inserted into the database")
        db_connection.commit()

    except:
        db_connection.close()
        print('Conexão fechada.')