from LEACH_create_basics import Sensor
from random import *


def zeros(row, column):
    re_list = []
    for x in range(row):
        temp_list = [0 for _ in range(column)]
        if row == 1:
            re_list.extend(temp_list)
        else:
            re_list.append(temp_list)

    return re_list


def start(sensors, my_model, round_number: int):
    CH = []

    # sink can't be a CH
    for sensor in sensors[:-1]:

        # If current sensor has energy left and has not been CH before And it is not dead
        # todo: keep either 'sensor.E > 0' or 'sensor.df == 0'

        if sensor.E > 0 and sensor.G <= 0:
            # Election of Cluster Heads
            temp_rand = uniform(0, 1)
            value = my_model.p / (1 - my_model.p * (round_number % round(1 / my_model.p)))
            print(f'for {sensor.id}, temprand = {temp_rand}, value = {value}')
            if temp_rand <= value:
                print(f"Adding {sensor.id} to CH")
                CH.append(sensor.id)
                sensor.type = 'C'
                sensor.G = round(1 / my_model.p) - 1


    return CH
