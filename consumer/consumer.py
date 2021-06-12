from kafka import KafkaConsumer
import kafka
import json
import mariadb
import sys
from data import *
from statistics import mean
import os 

#Utworzenie połączenia do bazy danych
try:
   conn = mariadb.connect(
      user=os.environ.get('DB_USER'),
      password=os.environ.get('DB_PASS'),
      host=os.environ.get('DB_HOST'),
      port=int(os.environ.get('DB_PORT')))
except mariadb.Error as e:
   print(f"Error connecting to MariaDB Platform: {e}")
   sys.exit(1)


if __name__ == "__main__":
    loop = True   
    
    #Pętla oczekująca na uruchomienie brokera, gdy połączenie jest pomyślne nawiązane, skrypt przechodzi dalej
    while loop == True: 
        try:
            consumer = KafkaConsumer(
                "temperature_data",
                bootstrap_servers='broker:9092',
                auto_offset_reset='earliest',
                group_id="consumer-group-a")
            print("starting the consumer")
            loop = False
        except kafka.errors.NoBrokersAvailable as e:
            pass
    
    #Przetworzenie odebranych wiadomości z brokera    
    for msg in consumer:
        #Utworzenie kursora
        cur = conn.cursor()
        #załadowanie danych
        temperature_data = json.loads(msg.value)
        #Przetworzenie ich na typ float
        temperature.append(float(ele) for ele in temperature_data)
        #Gdy otrzymamy 10 pomiarów to zapisujemy do bazy średnią
        if len(temperature) >= 10:
            #Obliczenie średniej oraz zamiana listy list na prostą listę
            avg = mean([ item for elem in temperature for item in elem])
            #Zaokrąglenie wyniku
            avg = round(avg,2)
            #Wyzerowanie listy
            temperature = []
            #Zapisanie danych do bazy danych
            cur.execute("INSERT INTO temperature.temperature_data(date, avgTemperature) VALUES (CURRENT_TIMESTAMP(), %s)", (avg,))
            #Wykonanie zapytania i zamknięcie połączenia
            conn.commit()
            cur.close()
    conn.close()
