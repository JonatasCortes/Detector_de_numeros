from .DefaultColors import Colors

class DefaultButton(Colors):
    
    def __init__(self, width:int, height:int, border:int , text:str,color:str|None = None, x_pos:int|None = None, y_pos:int|None = None):

        self.set_color(color)
        self.set_y_pos(y_pos)
        self.set_x_pos(x_pos)

        self.__width = width
        self.__height = height
        self.__border = border
        self.__text = text      
    
    def set_color(self, color: str|None):

        if color is None :
            self.__color = super.WHITE
        else:
            color = color.upper()
            color_dict = super().get_colorDict()
            try:
                self.__color = color_dict[color]
            except:
                raise ValueError("Nome inválido para cor")

    def get_colour (self)-> tuple[int,int,int]:
        return self.__color

    def isHover(self, mouse_pos: tuple[int, int]):
        if self.get_x_pos() <= mouse_pos[0] <= self.get_x_pos() + self.get_width() and self.get_y_pos() <= mouse_pos[1] <= self.get_y_pos() + self.get_height():
            return True
        return False

    def onHover(self, mouse_pos: tuple[int, int], hover_color: str):
        if self.isHover(mouse_pos):
            self.set_color(hover_color)
        else:
            self.set_color("white")

    def set_x_pos(self,position:int | None):
        if position is None:
            self.__x_pos = 0
        else:
            self.__x_pos = position
    def get_x_pos (self)-> int:
        return self.__x_pos
    
    
    def set_y_pos(self,position:int | None):
        if position is None:
            self.__y_pos = 0
        else:
            self.__y_pos = position     
    def get_y_pos (self)-> int:
        return self.__y_pos
    
    
    def get_height (self)-> int:
        return self.__height
    
    def get_width (self)-> int:
        return self.__width
    
    def get_border (self)-> int:
        return self.__border
    
    def get_text (self) -> str:
        return self.__text
    
    def get_button_rect(self)->tuple[int,int,int,int]:
        return self.get_x_pos(), self.get_y_pos(), self.get_width(), self.get_height()
        
        
        