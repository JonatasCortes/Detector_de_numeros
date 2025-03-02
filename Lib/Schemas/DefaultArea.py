from .DefaultColor import Colors

class DefaultArea(Colors):
    def __init__(self, width:int, height:int, x_pos:int|None=None, y_pos:int|None=None, color:str|None=None):
        
        self.set_x_pos(x_pos)
        self.set_y_pos(y_pos)
        self.set_color(color)

        self.__width = width
        self.__height = height

    def set_x_pos(self, position:int|None):
        if position is None:
            self.__x_pos = 0
        else:
            self.__x_pos = position

    def get_x_pos(self)-> int:
        return self.__x_pos
    
    def set_y_pos(self, position:int|None):
        if position is None:
            self.__y_pos = 0
        else:
            self.__y_pos = position

    def get_y_pos(self)-> int:
        return self.__y_pos
    
    def set_color(self, color:str|None):

        color_dict = super().get_colorDict()

        if color is None:
            self.__color = color_dict["BLACK"]
        else:
            self.__color = color_dict[color]

    def get_color(self):
        return self.__color
    
    def get_width(self)-> int:
        return self.__width
    
    def get_height(self)-> int:
        return self.__height