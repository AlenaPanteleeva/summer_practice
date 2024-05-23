class MetroStation:
    def __init__(self,name, x, y, postition):
        self.__name = name
        self.__x = x
        self.__y = y
        self.__position = postition
        self.__info_main_dir = {"last_train": 0, "last_train_steps": 0}
        self.__info_reverse_dir = {"last_train": 0, "last_train_steps": 0}

    def set_info(self, dir, last_train, last_train_steps):
        if dir > 0:
            self.__info_main_dir = {"last_train": last_train, "last_train_steps": last_train_steps}
        else:
            self.__info_reverse_dir = {"last_train": last_train, "last_train_steps": last_train_steps}

    def get_info(self, dir):
        if dir > 0:
            return self.__info_main_dir
        else:
            return self.__info_reverse_dir

    def get_name(self):
        return self.__name
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_position(self):
        return self.__position
