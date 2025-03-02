from .DefaultColors import Colors

class DefaultText(Colors):

    def __init__(self, text:str, color:str|tuple[int, int, int], size:int, x_pos:int|None = None, y_pos:int|None = None):

        self.set_color(color)
        self.set_y_pos(y_pos)
        self.set_x_pos(x_pos)

        self.__text = text
        self.__size = size

    def set_color(self, color: str|tuple[int, int, int]|None):
        if color is None:
            self.__color = "WHITE"
        elif type(color) == str:

            color = color.upper()
            color_dict = super().get_colorDict()

            try:
                self.__color = color_dict[color]
            except:
                raise ValueError("Nome inválido para cor")
        else:
            if 0 <= color[0] <= 255 and 0 <= color[1] <= 255 and 0 <= color[2] <= 255:
                self.__color = color
            else:
                raise ValueError("Valores inválidos para cor")
            
    def get_color (self)-> tuple[int,int,int]:
        return self.__color
            
    def set_x_pos(self, position:int|None):
        if position is None:
            self.__x_pos = 0
        else:
            self.__x_pos = position

    def get_x_pos (self)-> int:
        return self.__x_pos

    def set_y_pos(self, position:int|None):
        if position is None:
            self.__y_pos = 0
        else:
            self.__y_pos = position
    
    def get_y_pos(self)-> int:
        return self.__y_pos
    
    def get_text(self)-> str:
        return self.__text
    
    def get_size(self)-> int:
        return self.__size
    
