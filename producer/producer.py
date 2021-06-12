from kafka import KafkaProducer
import kafka
import json
from data import get_temperature
import time


def json_serializer(data):
    return json.dumps(data).encode("utf-8")

loop = True   
#Pętla działająca dopóki Broker nie zostanie uruchomiony (zapobiegnięcie crashu na początkus tartu skryptu)
while loop == True: 
    try:
        producer = KafkaProducer(bootstrap_servers=['broker:9092'],value_serializer=json_serializer)
        loop = False
    except kafka.errors.NoBrokersAvailable as e:
        pass


if __name__ == "__main__":
    #Ciągłe generowanie i wysyłanie danych do brokera co 2 sekundy
    while 1 == 1:
        temperature_data = get_temperature()
        print(temperature_data)
        producer.send("temperature_data", temperature_data)
        time.sleep(2)
    
