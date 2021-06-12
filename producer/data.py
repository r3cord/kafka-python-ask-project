import random

#Wylosowanie temperatury z przedziału <-20, 40>
def get_temperature():
    temperature = round(random.uniform(-20, 40),2)
    return temperature,


if __name__ == "__main__":
    print(get_temperature())
