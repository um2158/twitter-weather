from pyowm.owm import OWM


APIKEY = 'c793c1dd5e4c10cfa3d5a520cd1161bc'

if __name__ == '__main__':
    owm = OWM(APIKEY)
    reg = owm.city_id_registry()
    list_of_tuples = ny = reg.ids_for('New York', country='NY')
    print(list_of_tuples)
    mgr = owm.weather_manager()
    weather = mgr.weather_at_place('New York').weather
    print(weather.status)
    print(weather.detailed_status)
    temp_dict_celsius = weather.temperature('celsius')
    print(temp_dict_celsius)
    wind_dict_in_meters_per_sec = weather.wind()
    print(wind_dict_in_meters_per_sec)
    # historian = mgr.station_hour_history(5128638)
    # print(historian.temperature_series(unit="celsius"))       # now in Celsius



