import random
import Metro
class Train:
    def __init__(self, direction:int, speed: int, position:int):
        self.__direction = direction  # Направление
        self.__speed = speed  # Скорость
        self.__default_speed = speed  # Скорость по умолчанию
        self.__position = position  # Позиция в метро
        self.__status = True  # Состояние поезда
        self.__status_update = False  # Состояние изменилось только что
        self.__status_count = 0  # Время в текущем состоянии

    def set_speed(self, speed):
        self.__speed = speed

    def set_direction(self, direction):
        self.__direction = direction

    def get_status(self):
        return self.__status

    def get_status_count(self):
        return self.__status_count

    def get_status_update(self):
        return self.__status_update

    def get_speed(self):
        return self.__speed

    def get_direction(self):
        return self.__direction

    def get_position(self):
        return self.__position

    def on_station(self, metro):  # Проверяем, находимся ли мы на станции
        for station in metro.get_points():
            if self.__position == station.get_position():
                return station
        return False

    def __get_start_station(self, metro):  # Получаем самую левую станцию в метро (один из концов ветки)
        return min(metro.get_points(), key=Metro.MetroStation.get_position).get_position()

    def __get_end_station(self, metro):  # Получаем самую правую станцию в метро (один из концов ветки)
        return max(metro.get_points(), key=Metro.MetroStation.get_position).get_position()

    def update(self, metro, step):
        if self.__status:
            station = self.on_station(metro)
            if station:
                if self.__speed > 0:
                    self.__speed = 0
                    self.__status_count = 6
                    self.__status_update = True
                    station.set_info(self.__direction, step, random.randint(4, 8))
                else:
                    self.__status_count -= 1
                    self.__status_update = False
                    if self.__status_count == 0:
                        self.__speed = self.__default_speed
                if self.__direction > 0 and self.__get_end_station(metro) <= self.__position and self.__speed > 0:
                    self.__direction *= -1
                elif self.__direction < 0 and self.__get_start_station(metro) >= self.__position and self.__speed > 0:
                    self.__direction *= -1
            if random.randint(0, 200) == 0:
                self.__speed = 0
                self.__status = False
                self.__status_count = random.randint(6, 20)
                self.__status_update = True
                return
            self.__position += self.__speed * self.__direction
        else:  # Если поезд сломан
            self.__status_update = False
            self.__status_count -= 1
            if not self.__status_count:
                self.__status = True
                self.__speed = self.__default_speed








            
