weather_translate = {
    "Thunderstorm": "Гроза",
    "Drizzle": "Мелкий дождь",
    "Rain": "Дождь",
    "Snow": "Снег",
    "Clear": "Ясно",
    "Clouds": "Облачно",
}

weather_emoji = {
    "Thunderstorm": "🌩️",
    "Drizzle": "🌧️",
    "Rain": "🌧️",
    "Snow": "❄️",
    "Clear": "🌞",
    "Clouds": "🌥️",
}


def get_coordinates_from_city_button(cities: dict, button_city: str, button_country: str, button_state: str) -> dict | None:
    coordinates = dict()
    for city in cities:
        if city["name"] == button_city and city["country"] == button_country and city["state"] == button_state:
            coordinates['latitude'] = city["lat"]
            coordinates['longitude'] = city["lon"]
            return coordinates
    

def create_current_weather_report(response: dict) -> str:
    report = ""
    if response['weather'][0]['main'] in weather_translate.keys():
        report += weather_translate[response['weather'][0]['main']]
    else: 
        report += response['weather'][0]['main']

    if response['weather'][0]['main'] in weather_emoji.keys():
        report += " " + weather_emoji[response['weather'][0]['main']] + "\n"
    else:
        report += "\n"

    report += response['weather'][0]['description'] + "\n"
    report += "Температура: " + str(round(response['main']['temp'] - 273.15, 2)) + "\n"
    report += "Ощущается как: " + str(round(response['main']['feels_like'] - 273.15, 2)) + "\n"
    report += "Давление: " + str(response['main']['pressure']) + "\n"
    report += "Скорость ветера: " + str(response['wind']['speed']) + "\n"
    report += "Облачность (в процентах): " + str(response['clouds']['all'])
    return report


def create_air_polution_report(response: dict) -> str:
    report = ""
    report += "Индекс качества воздуха: " + str(response['list'][0]['main']['aqi']) + "\n"
    report += "Концентрация CO: " + str(response['list'][0]['components']['co']) + " мкг/м3\n"
    report += "Концентрация NO: " + str(response['list'][0]['components']['no']) + " мкг/м3\n"
    report += "Концентрация NO\u2082: " + str(response['list'][0]['components']['no2']) + " мкг/м3\n"
    report += "Концентрация O3: " + str(response['list'][0]['components']['o3']) + " мкг/м3\n"
    report += "Концентрация SO\u2082: " + str(response['list'][0]['components']['so2']) + " мкг/м3\n"
    report += "Концентрация PM\u2082.\u2085: " + str(response['list'][0]['components']['pm2_5']) + " мкг/м3\n"
    report += "Концентрация PM\u2081\u2080: " + str(response['list'][0]['components']['pm10']) + " мкг/м3\n"
    report += "Концентрация NH\u2083: " + str(response['list'][0]['components']['nh3']) + " мкг/м3\n"
    return report


def create_weather_forecast(response: dict) -> list[str]:
    report_list = []
    forecasts = response['list']
    current_date = ""
    report = ""
    for forecast in forecasts:
        if forecast['dt_txt'][:10] != current_date:
            if report != "":
                report_list.append(report)
            report = ""
            current_date = forecast['dt_txt'][:10]
            report += current_date + "\n"

        report += forecast['dt_txt'][11:16] + "\n"
        if forecast['weather'][0]['main'] in weather_translate.keys():
            report += weather_translate[forecast['weather'][0]['main']]
        else: 
            report += forecast['weather'][0]['main']

        if forecast['weather'][0]['main'] in weather_emoji.keys():
            report += " " + weather_emoji[forecast['weather'][0]['main']] + "\n"
        else:
            report += "\n"

        report += forecast['weather'][0]['description'] + "\n"
        report += "Температура: " + str(round(forecast['main']['temp'] - 273.15, 2)) + "\n"
        report += "Ощущается как: " + str(round(forecast['main']['feels_like'] - 273.15, 2)) + "\n"
        report += "Давление: " + str(forecast['main']['pressure']) + "\n"
        report += "Скорость ветера: " + str(forecast['wind']['speed']) + "\n"
        report += "Облачность (в процентах): " + str(forecast['clouds']['all']) + "\n\n"

    return report_list