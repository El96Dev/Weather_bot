# Описание
Телеграм бот для получения уведомлений о погоде с использованием API сервиса OpenWeatherMap.
# Функционал
Данный бот позволяет получать актуальные данные о текущей погоде, прогнозе погоды на сдедующие 5 дней и загрязнении воздуха.
Также пользователь может подписаться на ежедневные уведомления о текущей погоде и прогнозе погоды на 5 дней. Время отправки уведомлений может быть выбрано пользователем:
  * утренние (08:00)
  * дневные (12:00)
  * вечерние (18:00)
    
Доступны два варианта указания геолокации: широта и долгота или название населённого пункта. 
Каждый пользователь может подписаться не более чем на 2 уведомления каждого типа (текущая погода или прогноз погоды на 5 дней). 
Уведомления о погоде можно удалять или редактировать (изменение времени отправки или геолокации).

# Инструкция по запуску
Для запуска бота необходимо зарегестрироваться на сайте 
https://openweathermap.org/, зайти во вкладку профиля 'My API keys' и сгенерировать API ключ.

Также необходимо использовать телеграм бота BotFather https://telegram.me/BotFather. Для создания нового бота и получения токена воспользуйтесь командой '/newbot'.

Далее в папке с проектом создайте файл .env и добавьте в него полученный API ключ и токен: 
``` 
OPEN_WEATHER_TOKEN=<API ключ>
TELEGRAM_TOKEN=<Токен телеграм бота>
```
Для запуска проекта установите Docker, откройте терминал в папке проекта и введите команду `docker compose up --build`
## Вермя отправки уведомлений
Время отправки утренних, дневных или вечерних уведомлений можно изменить в файле config.json. Для изменения времени отправки замените значение по умолчанию на необходимое: 
```
{
    "morning_notifications_time": "08:00",
    "day_notifications_time": "12:00",
    "evening_notifications_time": "18:00"
}
```
