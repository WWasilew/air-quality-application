import air_quality
import sys
from matplotlib import pyplot as plt


def list_stations(a):
    all_stations = air_quality.get_stations()
    for station in all_stations:
        print(f'{station.get_id()}\t{station}')


def main(arguments):
    """
    From which station do you want to create plot?
    """
    target_city = 'Warszawa'
    target_sensor = 10955

    all_stations = [
        station for station in air_quality.get_stations()
        if target_city and station.get_city_name() == target_city
        ]
    for targeted in all_stations:
        if targeted.get_id() == target_sensor:
            station = targeted
    all_sensors = station.sensors()
    for sensor in all_sensors:
        readings = sensor.readings()
        keys = [reading.date for reading in readings]
        values = [reading.value for reading in readings]
        plt.plot(keys, values, 'o-', label=sensor.get_name())
    plt.title(label=station.get_name())
    plt.xticks(rotation=30, fontsize='xx-small', horizontalalignment='right')
    plt.legend()
    figure = plt.gcf()  # to save
    figure.savefig('station.png')
    plt.show()


if __name__ == "__main__":
    main(sys.argv)
