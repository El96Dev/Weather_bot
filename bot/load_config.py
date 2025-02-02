import json 

from models import NotificationsTime


class Config:
    def __init__(self, file_path: str):
        with open(file_path, 'r') as file:
            if file_path.endswith('.json'):
                conf_json = json.load(file)
                self.morning_notifications_time = conf_json.get('morning_notifications_time', "08:00")
                self.day_notifications_time = conf_json.get('day_notifications_time', "12:00")
                self.evening_notifications_time = conf_json.get('evening_notifications_time', "18:00")

                self.morning = self.MorningConfig(self.morning_notifications_time)
                self.day = self.DayConfig(self.day_notifications_time)
                self.evening = self.EveningConfig(self.evening_notifications_time)
            else:
                raise ValueError("Unsupported file format. Please, use .json format.")
    
    class MorningConfig:
        def __init__(self, time_str: str):
            self.time_str = time_str

        def get_notifications_time(self) -> str:
            return self.time_str
            
        def get_hour(self) -> int:
            try:
                hour, _ = self.time_str.split(':')
                return int(hour)
            except ValueError:
                raise ValueError(f"Invalid time format: {self.time_str}. Expected 'HH:MM'.")
            
        def get_minute(self) -> int:
            try:
                _, minute = self.time_str.split(':')
                return int(minute)
            except ValueError:
                raise ValueError(f"Invalid time format: {self.time_str}. Expected 'HH:MM'.")

    class DayConfig:
        def __init__(self, time_str: int):
            self.time_str = time_str

        def get_notifications_time(self) -> str:
            return self.time_str
        
        def get_hour(self) -> int:
            try:
                hour, _ = self.time_str.split(':')
                return int(hour)
            except ValueError:
                raise ValueError(f"Invalid time format: {self.time_str}. Expected 'HH:MM'.")
            
        def get_minute(self) -> int:
            try:
                _, minute = self.time_str.split(':')
                return int(minute)
            except ValueError:
                raise ValueError(f"Invalid time format: {self.time_str}. Expected 'HH:MM'.")

    class EveningConfig:
        def __init__(self, time_str: str):
            self.time_str = time_str

        def get_notifications_time(self) -> str:
            return self.time_str
        
        def get_hour(self) -> int:
            try:
                hour, _ = self.time_str.split(':')
                return int(hour)
            except ValueError:
                raise ValueError(f"Invalid time format: {self.time_str}. Expected 'HH:MM'.")
            
        def get_minute(self) -> int:
            try:
                _, minute = self.time_str.split(':')
                return int(minute)
            except ValueError:
                raise ValueError(f"Invalid time format: {self.time_str}. Expected 'HH:MM'.")
    
    def get_notifications_time_value(self, notifications_time: NotificationsTime) -> str:
        if notifications_time == NotificationsTime.MORNING:
            return self.morning_notifications_time
        elif notifications_time == NotificationsTime.DAY:
            return self.day_notifications_time
        elif notifications_time == NotificationsTime.EVENING:
            return self.evening_notifications_time


config = Config("config.json") 