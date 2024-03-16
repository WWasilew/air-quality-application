import requests
from datetime import datetime


urls = {
    'findAll': 'https://api.gios.gov.pl/pjp-api/rest/station/findAll',
    'sensors': 'https://api.gios.gov.pl/pjp-api/rest/station/sensors/{stationId}',
    'getData': 'https://api.gios.gov.pl/pjp-api/rest/data/getData/{sensorId}',
    'index': 'https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{stationId}'
}


def get_stations():
    stations = requests.get(urls['findAll']).json()
    all_stations = []
    for station_data in stations:
        station = Station(station_data)
        all_stations.append(station)
    return all_stations


class AirApiObject:
    def __init__(self, data):
        self._data = data

    def get_id(self):
        return self._data['id']

    def _get(self, key_word):
        return self._data[key_word]


class Station(AirApiObject):
    def get_name(self):
        return self._data['stationName']

    def get_position(self):
        lat = self._get('gegrLat')
        lon = self._get('gegrLon')
        return (float(lat), float(lon))

    def get_city_name(self):
        return self._get('city')['name']

    def city_data(self):
        return self._get('city')

    def sensors(self):
        id = self.get_id()
        all_sensors = requests.get(urls['sensors'].format(stationId=id)).json()
        return [Sensor(self, sensor) for sensor in all_sensors]

    def __str__(self):
        return self.get_name()


class Sensor(AirApiObject):
    def __init__(self, station, data):
        super().__init__(data)
        self._station = station

    def get_name(self):
        return self._get('param').get('paramName')

    def get_code(self):
        return self._get('param').get('paramCode')

    def get_param_data(self):
        return self._get('param')

    def which_station(self):
        return self._station

    def readings(self):
        """
        result - dictionary
        """
        id = self.get_id()
        result = requests.get(urls['getData'].format(sensorId=id)).json()
        key = result['key']
        values = result['values']
        return [
            Reading(self,
                    key,
                    datetime.fromisoformat(value['date']),
                    value['value'])
                    for value in values
        ]


class Reading:
    def __init__(self, sensor, key, date, value):
        self._sensor = sensor
        self.key = key
        self.date = date
        self.value = value

    def __str__(self):
        return f'{self.key}: {self.value} on {self.date}'

    def get_sensor(self):
        return self._sensor
