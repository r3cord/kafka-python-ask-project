# kafka-python-ask-project
Projekt wykonany na studia z ASK

## Zależności:
Aby uruchomić aplikację porzebujemy:
* [Docker](https://docs.docker.com/engine/install/ubuntu/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Uruchomienie:
W celu uruchomienia aplikacji należy pobrać ją do swojego katalogu. Następnie w pliku [docker-compose.yml](https://github.com/r3cord/kafka-python-ask-project/blob/main/docker-compose.yml) edytujemy /home/daniel/ASK2/ przy volumes na własną ścieżkę, w której chcemy zapisywać bazę danych.

Następnie przechodzimy do katalogu [consumer](https://github.com/r3cord/kafka-python-ask-project/tree/main/consumer) i budujemy obraz dla Dockera. Robimy to poleceniem:
```bash
sudo docker build -t python-consumer:1 .
```
Kolejnym krokiem jest zbudowanie obrazu producera. Robimy to w katalogu [producer](https://github.com/r3cord/kafka-python-ask-project/tree/main/producer) poleceniem:
```bash
sudo docker build -t python-producer:1 .
```

Teraz przed samym uruchomieniem aplikacji musimy utworzyć bazę danych. Możemy zrobić to w następujący sposób:
Najpierw uruchamiamy kontener z bazą danych 
```bash
sudo docker run --name mariadb -v /home/daniel/ASK2/:/var/lib/mysql -e 
MARIADB_ROOT_PASSWORD=Zaq12wsx -d mariadb 
```
Ścieżkę „/home/daniel/ASK2/” zamieniamy na taką samą jaką ustawiliśmy w pliku [docker-compose.yml](https://github.com/r3cord/kafka-python-ask-project/blob/main/docker-compose.yml).
Następnie logujemy się do bazy danych poleceniem: 
```bash
sudo docker exec -it mariadb mysql -u root -p 
```
Wpisujemy hasło „Zaq12wsx” 

CZĘŚĆ SQL:
```SQL
#Tworzymy nową bazę danych: 
CREATE DATABASE temperature; 
#Wybieramy ją jako bazę, którą chcemy używać: 
USE temperature; 
#Następnie tworzymy tabelę: 
CREATE TABLE temperature_data(id INT PRIMARY KEY AUTO_INCREMENT, date TIMESTAMP, avgTemperature FLOAT); 
#Potem tworzymy użytkownika, którym będziemy się logować: 
CREATE USER 'python'@'%' IDENTIFIED BY 'Zaq12wsx'; 
#I na sam koniec dodajemy mu wszystkie uprawnienia do utworzonej bazy: 
GRANT ALL PRIVILEGES ON temperature.* TO 'python'@'%'; 
#Przeładowywujemy uprawnienia: 
FLUSH PRIVILEGES;
```
Wychodzimy z bazy danych i kontenera wpisując exit (czasami trzeba wpisać dwa razy). 

Usuwamy kontener z serwerem bazy danych, ale dzięki volumenowi baza danych zostanie 
przechowana i wykorzystana w naszej aplikacji. 
```bash
sudo docker rm -f mariadb 
```

Teraz możemy odpalić naszą aplikację poleceniem znajdując się w katalogu głównym aplikacji: 
```bash
sudo docker-compose up 
```

Aplikacja powinna się w tym momencie uruchomić i zacząć swoje działanie (generować dane, przesyłać je przez kafkę, obliczać średnią i przesyłać do bazy danych).


