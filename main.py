import Metro
import Train
import Window

point1 = Metro.MetroStation('Князевская',60, 100, 0)
point2 = Metro.MetroStation('Бабушкинская',170, 250, 200)
point3 = Metro.MetroStation('Баррикадная',300, 300, 400)
point4 = Metro.MetroStation('Лефортово',450, 300, 550)
point5 = Metro.MetroStation('Люблино',600, 200, 750)
point6 = Metro.MetroStation('Семеновская',750, 100, 1000)
point7 = Metro.MetroStation('Сокол ',900, 100, 1270)

point5_1 = Metro.MetroStation('Митино',250, 100, 400)
point5_2 = Metro.MetroStation('Текстильщики',400, 100, 550)
point5_3 = Metro.MetroStation('Озерная',800, 250, 900)

metro = Metro.Metro()
metro5 = Metro.Metro()
metro.add_station(point1)
metro.add_station(point2)
metro.add_station(point3)
metro.add_station(point4)
metro.add_station(point5)
metro.add_station(point6)
metro.add_station(point7)
metro5.add_station(point5_1)
metro5.add_station(point5_2)
metro5.add_station(point5)
metro5.add_station(point5_3)

for i in range(7):
    metro.add_train(Train.Train(1, 1, 200 * i))
for i in range(5):
    metro.add_train(Train.Train(-1, 1, 1200 - i * 250))
metro5.add_train(Train.Train(1, 1, 450))
metro5.add_train(Train.Train(1, 1, 700))
metro5.add_train(Train.Train(-1, 1, 600))

    
win = Window.Window([metro, metro5])
win.mainloop()

