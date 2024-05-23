from MetroStation import MetroStation
class Metro:
    def __init__(self):
        self.__stations = []  # Список станций
        self.__trains = []  # Список поездов
        self.__sum_speed = 0  # Суммарная скорость
        self.__steps = 0  # Время с начала моделирования
        self.__breakdown_count = 0  # Количество аварий
        self.__breakdown_steps = 0  # Суммарное время аварий
        self.__on_station_steps = 0  # Суммарное время остановок на станциях
        self.__on_station_count = 0  # Суммарное количество остановок на станциях
    
    def add_train(self, train):
        if train not in self.__trains:
            self.__trains.append(train)
    
    def add_station(self, station):
        self.__stations.append(station)

    def get_steps(self):
        return self.__steps

    def get_breakdown_count(self):
        return self.__breakdown_count

    def get_breakdown_steps(self):
        return self.__breakdown_steps

    def get_on_station_count(self):
        return self.__on_station_count

    def get_on_station_steps(self):
        return self.__on_station_steps
    
    def get_sum_speed(self):
        return self.__sum_speed
        
    def get_trains(self):
        return self.__trains
    
    def get_points(self):
        return self.__stations

    def update(self):
        self.__steps += 1
        for train in self.__trains:
            train.update(self, self.__steps)
            
            if train.get_status():
                if train.on_station(self):
                    if train.get_status_update():
                        self.__on_station_count += 1
                    self.__on_station_steps += 1
                self.__sum_speed += train.get_speed() * 80
            else:
                if train.get_status_update():
                    self.__breakdown_count += 1
                self.__breakdown_steps += 1







