import tkinter
from tkinter import ttk

class Table(ttk.Treeview):
    def __init__(self, parent, columns, **kwargs):
        super().__init__(parent, columns=columns, **kwargs)

        self.rev = {f"#{x}": False for x in range(len(columns) + 1)}

        self.column("#0", width=0, stretch=tkinter.NO)
        self.heading("#0", text="", anchor=tkinter.CENTER, command=lambda: self.sort_column("#0"))

        for i, column in enumerate(columns, start=1):
            self._add_column(column, i)

        self._id = 0

    def _add_column(self, name, i):
        s = f"#{i}"
        self.column(name, anchor=tkinter.CENTER, width=80)
        self.heading(name, text=name, anchor=tkinter.CENTER, command=lambda: self.sort_column(s))

    def add_row(self, *args):
        args = list(args)
        for i in range(len(args)):
            if type(args[i]) == bool:
                args[i] = "+" if args[i] else "-"
        self.insert(parent='', index='end', iid=self._id, text='', values=args)
        self._id += 1

    def edit_row(self, *args, key=0):
        children = self.get_children()
        for child in children:
            if self.set(child, key) == args[key]:
                for i, val in enumerate(args):
                    self.set(child, i, val)
                return

    def sort_column(self, col):
        l = [(self.set(k, col), k) for k in self.get_children('')]
        l.sort(reverse=self.rev[col], key=lambda x: int(x[0]) if x[0].isdigit() else str(x[0]))

        for k in self.rev.keys():
            self.heading(k, text=self.heading(k, "text").replace("v", "").replace("^", ""))
        self.heading(col, text=["^", "v"][self.rev[col]] + self.heading(col, "text"))

        self.rev[col] = not self.rev[col]
        for index, (val, k) in enumerate(l):
            self.move(k, '', index)


class Window(tkinter.Tk):
    def __init__(self, metro):
        super().__init__()

        self.geometry("1000x600+200+100")
        self.title("Симуляция метро")

        self.__metro = metro
        self.__pause = False

        self.__canvas = tkinter.Canvas(self, bg="gray")
        self.__table = Table(self, ["Хар-ка", "Значение"], show="tree")
        self.__time_label = tkinter.Label(self, text="Время: 00:00")
        self.__canvas.pack(expand=True, fill=tkinter.BOTH)
        self.__time_label.pack(fill=tkinter.BOTH)
        self.__table.pack(fill=tkinter.BOTH)

        self.__table.add_row("Средняя скорость", 0)
        self.__table.add_row("Среднее время остановки", 0)
        self.__table.add_row("Количество поломок", 0)
        self.__table.add_row("Среднее время поломки", 0)

        self.__canvas.bind("<ButtonRelease-1>", self.pause)
        
        self.__update()

    def pause(self, event):
        self.__pause = not self.__pause
    
    def __clear(self):
        self.__canvas.delete("all")
    def __draw_station(self, metro):
        points = metro.get_points()
        last_x = None
        last_y = None
        last_position = None
        station_colors = ["red", "blue", "green", "orange", "purple", "yellow", "cyan"]  # Список цветов для станций
        station_color_index = 0  # Индекс цвета станции
        for point in points:
            x = point.get_x()
            y = point.get_y()
            position = point.get_position()
            name = point.get_name()

            self.__canvas.create_text(x, y, fill="white", text="M", font=("Arial", 10, "bold"))
            self.__canvas.create_text(x, y - 20, fill="black", text=name, font=("Arial", 10))

            dot_color = station_colors[station_color_index]  # Выбираем цвет для текущей станции
            dot = self.__canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=dot_color,
                                            width=0)
            self.__canvas.tag_lower(dot)

            if last_x and last_y:
                line = self.__canvas.create_line(last_x, last_y, x, y, fill="red", width=2)
                self.__canvas.tag_lower(line)
                self.__draw_trains(metro, last_position, position, last_x, last_y, x, y)
            last_x = x
            last_y = y
            last_position = position
            station_color_index = (station_color_index + 1) % len(
                station_colors)  # Обновляем индекс цвета для следующей станции

    def __draw_trains(self, metro, point0, point1, x0, y0, x1, y1):
        for train in metro.get_trains():
            color = "green"
            if not train.get_status():
                color = "orange"
            if train.get_direction() == 1 and point0 <= train.get_position() < point1:
                x = x0 + int((x1 - x0) / (point1 - point0) * (train.get_position() - point0))
                y = y0 + int((y1 - y0) / (point1 - point0) * (train.get_position() - point0))
                y += 7
                dot = self.__canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, width=0)
                self.__canvas.tag_raise(dot)
            elif train.get_direction() == -1 and point0 < train.get_position() <= point1:
                x = x0 + int((x1 - x0) / (point1 - point0) * (train.get_position() - point0))
                y = y0 + int((y1 - y0) / (point1 - point0) * (train.get_position() - point0))
                y -= 7
                dot = self.__canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, width=0)
                self.__canvas.tag_raise(dot)

    def __draw_station_info(self, x, y, dir, last_train, last_train_steps):
        hours = int(self.__metro[0].get_steps() / 60)
        minutes = int(self.__metro[0].get_steps() % 60)

        self.__canvas.create_rectangle(x, y, x + 120, y + 55, fill="white")
        self.__canvas.create_rectangle(x, y, x + 120, y + 15, fill="white")
        self.__canvas.create_rectangle(x, y + 15, x + 120, y + 35, fill="white")
        self.__canvas.create_rectangle(x, y + 35, x + 120, y + 55, fill="white")
        
        if dir == 1:
            self.__canvas.create_rectangle(x + 30, y + 5, x + 60, y + 10, fill="orange", width=0)
            self.__canvas.create_polygon(x + 60, y + 1, x + 80, y + 7, x + 60, y + 14, fill="orange")
        else:
            self.__canvas.create_rectangle(x + 80, y + 5, x + 50, y + 10, fill="orange", width=0)
            self.__canvas.create_polygon(x + 50, y + 1, x + 30, y + 7, x + 50, y + 14, fill="orange")

        line1x = x + 60
        line1y = y + 25
        self.__canvas.create_text(line1x, line1y, fill="black", text=f"{last_train}м назад")
        self.__canvas.create_text(line1x, line1y + 20, fill="black", text=f"Стоянка: {last_train_steps}м")

    def __draw_info(self):
        hours = int(self.__metro[0].get_steps() / 60)
        minutes = int(self.__metro[0].get_steps() % 60)
        self.__time_label.config(text=f"Время {hours:02}:{minutes:02}")

        avg_speed = self.__metro[0].get_sum_speed() / self.__metro[0].get_steps() / len(self.__metro[0].get_trains())
        self.__table.edit_row("Средняя скорость",
                             f"{avg_speed:0.2f} км/ч.")
        self.__table.edit_row("Среднее время остановки",
                             f"{self.__metro[0].get_on_station_steps() / self.__metro[0].get_on_station_count():0.1f} минут")
        self.__table.edit_row("Количество поломок",
                             f"{self.__metro[0].get_breakdown_count()}")
        self.__table.edit_row("Среднее время поломки",
                             f"{self.__metro[0].get_breakdown_steps() / (self.__metro[0].get_breakdown_count() or 1):0.1f} минут")

        if self.__pause:
            for metro in self.__metro:
                for i, station in enumerate(metro.get_points()):
                    if i != 0:
                        station_info = station.get_info(-1)
                        last_train = self.__metro[0].get_steps() - station_info["last_train"]
                        last_train_steps = station_info["last_train_steps"]
                        self.__draw_station_info(station.get_x() - 60, station.get_y() - 60, -1, last_train, last_train_steps)
                    if i != len(metro.get_points()) - 1:
                        station_info = station.get_info(1)
                        last_train = self.__metro[0].get_steps() - station_info["last_train"]
                        last_train_steps = station_info["last_train_steps"]
                        self.__draw_station_info(station.get_x() - 60, station.get_y() + 10, 1, last_train, last_train_steps)
    
    def __draw_update(self, metro, clear=True):
        if clear:
            self.__clear()
        self.__draw_station(metro)
    
    def __update(self):
        clear = True
        for metro in self.__metro:
            if not self.__pause:
                metro.update()
            self.__draw_update(metro, clear=clear)
            clear = False
        self.__draw_info()
        self.after(100, self.__update)











