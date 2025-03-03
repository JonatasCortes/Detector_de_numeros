from time import process_time_ns
import json
import sys
import numpy as np
import pygame
from pygame.locals import *
from Lib.Schemas.DefaultButton import DefaultButton
from Lib.Schemas.DefaultText import DefaultText
from Lib.Schemas.DefaultArea import DefaultArea
from Lib.Schemas.DefaultColor import Colors

#importa o dicionario com todas as cores do projeto

colors = Colors()
color_dict = colors.get_colorDict()

#define as informações da tela

screen_width = 640
screen_height = 480

#inicia a tela em que o programa será executado

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height)) #criacao da tela
clock = pygame.time.Clock()
pygame.display.set_caption("Number Detector") #titulo da janela


# region BUTTONS

guess_button = DefaultButton(height=50,width=220,border=5,text="GUESS NUMBER",color="WHITE")
guess_button.set_x_pos((screen_width//2)-guess_button.get_width()//2)
guess_button.set_y_pos((screen_height//2)-guess_button.get_height())

train_model_button = DefaultButton(width=220, height=50,border= 5, color="WHITE", text= "TRAIN MODEL")
train_model_button.set_x_pos(guess_button.get_x_pos())
train_model_button.set_y_pos(guess_button.get_y_pos() + guess_button.get_height() + 10)

exit_button = DefaultButton(width=220, height=50, border=5, color="WHITE", text= "EXIT")
exit_button.set_x_pos(guess_button.get_x_pos())
exit_button.set_y_pos(train_model_button.get_y_pos()+ train_model_button.get_height() + 10)

return_button = DefaultButton(width=220, height=50, border=5, color="WHITE", text="RETURN")
return_button.set_x_pos(screen_width-return_button.get_width()-20)
return_button.set_y_pos(screen_height-return_button.get_height()-50)

erase_button = DefaultButton(width=220, height=50, border=5, color="MAGENTA", text="ERASE")
erase_button.set_x_pos(return_button.get_x_pos())
erase_button.set_y_pos(return_button.get_y_pos()-return_button.get_height()-20)

trainDB_button = DefaultButton(width=220, height=50, border=5, color="WHITE", text="TRAIN DB")
trainDB_button.set_x_pos(erase_button.get_x_pos())
trainDB_button.set_y_pos(erase_button.get_y_pos()-erase_button.get_height()-20)
# endregion

# region AREAS

drawing_area = DefaultArea(width=(return_button.get_x_pos()-20), height=screen_height)

typing_area = DefaultArea(width=220, height=50)
typing_area.set_x_pos(trainDB_button.get_x_pos())
typing_area.set_y_pos(trainDB_button.get_y_pos()-trainDB_button.get_height()-100)
typing_area.set_color("WHITE")
# endregion

# region TEXTS

main_menu_title = DefaultText(text="Number Detector", color="CYAN", size=100)
main_menu_title.set_x_pos(screen_width//2)
main_menu_title.set_y_pos(guess_button.get_y_pos() - 100)

typing_text = DefaultText(text="", color="BLACK", size=50)
typing_text.set_x_pos(typing_area.get_x_pos()+typing_area.get_width()//2)
typing_text.set_y_pos(typing_area.get_y_pos()+typing_area.get_height()//2)

added_to_db_text = DefaultText(text="ADDED TO DB!", color="CYAN", size=50)
added_to_db_text.set_x_pos(drawing_area.get_width()//2)
added_to_db_text.set_y_pos((drawing_area.get_height()//2)-40)

press_erase_text = DefaultText(text="PRESS ERASE", color="CYAN", size=50)
press_erase_text.set_x_pos(added_to_db_text.get_x_pos())
press_erase_text.set_y_pos(added_to_db_text.get_y_pos()+40)

to_continue_text = DefaultText(text="TO CONTINUE", color="CYAN", size=50)
to_continue_text.set_x_pos(press_erase_text.get_x_pos())
to_continue_text.set_y_pos(press_erase_text.get_y_pos()+40)

# endregion

#region FUNCTIONS

def mouse_on_area(mouse_pos, area_info:DefaultArea):
    if area_info.get_x_pos() <= mouse_pos[0] <= area_info.get_x_pos() + area_info.get_width() and area_info.get_y_pos() <= mouse_pos[1] <= area_info.get_y_pos() + area_info.get_height():
        return True
    else:
        return False

def draw_text(text_info:DefaultText):

    font = pygame.font.Font(None, text_info.get_size())

    text_surface = font.render(text_info.get_text(), True, text_info.get_color())
    text_rect = text_surface.get_rect(center=(text_info.get_x_pos(), text_info.get_y_pos()))

    screen.blit(text_surface, text_rect)

def draw_button(button_info:DefaultButton):

    rect = button_info.get_x_pos(),button_info.get_y_pos(),button_info.get_width(),button_info.get_height()
    pygame.draw.rect(screen, button_info.get_colour(), rect, button_info.get_border())

    text_info = DefaultText(text=button_info.get_text(), color=button_info.get_colour(), size=36)
    text_info.set_x_pos(button_info.get_x_pos()+(button_info.get_width()//2))
    text_info.set_y_pos(button_info.get_y_pos()+(button_info.get_height()//2))

    if button_info.get_text() != "":
        draw_text(text_info)

def numberImageToMatrix():
    screen_as_array = pygame.surfarray.array3d(screen)
    screen_as_array = np.rot90(screen_as_array)
    screen_as_array = screen_as_array[::-1]
    screen_as_array = screen_as_array[0:drawing_area.get_width(), 0:drawing_area.get_height()]

    screen_as_boolean_array = np.all(screen_as_array == color_dict["DRAWING_COLOR"], axis=-1)
    coordinates_of_drawn_pixels = np.argwhere(screen_as_boolean_array)

    min_y, min_x = coordinates_of_drawn_pixels.min(axis=0)
    max_y, max_x = coordinates_of_drawn_pixels.max(axis=0)

    screen_as_boolean_array = screen_as_boolean_array[min_y:max_y+1, min_x:max_x+1]
    binary_array = screen_as_boolean_array.astype(int)

    if binary_array.size == 0:
        return None

    return binary_array

def numberDensityVector(numberMatrix):
    height, width = numberMatrix.shape
    numerber_of_sections = 4

    number_vector = []

    step_H = height//numerber_of_sections
    step_W = width//numerber_of_sections

    for index1 in range(numerber_of_sections):
        for index2 in range(numerber_of_sections):
            min_x = step_W*index2
            max_x = step_W*(index2+1) if index2 < (numerber_of_sections-1) else width
            min_y = step_H*index1
            max_y = step_H*(index1+1) if index1 < (numerber_of_sections-1) else height

            section = numberMatrix[min_y : max_y+1, min_x : max_x+1]

            num_pixels_desenhados = 0
            num_pixels_pretos = 0

            for row in section:
                for pixel in row:
                    if pixel == 1:
                        num_pixels_desenhados += 1
                    else:
                        num_pixels_pretos += 1

            section_density = num_pixels_desenhados/(num_pixels_desenhados+num_pixels_pretos)
            number_vector.append(section_density)

    return tuple(number_vector)

def addNumberToDataBase(file, number, number_list):

    numberMatrix = numberImageToMatrix()
    if numberMatrix is None:
        return False

    num_vector = numberDensityVector(numberMatrix)

    new_number = {number : num_vector}
    number_list.append(new_number)

    with open(file, "w", encoding="utf-8") as arquivo:
        json.dump(number_list, arquivo, indent=4)

    return True

# endregion

#função que exibe o menu principal da aplicação
def main_menu():

    running = True
    while running:

        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                running = False

            guess_button.changeColorOnHover(mouse_pos,"MAGENTA")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if guess_button.isHover(mouse_pos):
                    guessNumber()
                    print(guess_button.get_colour())

            train_model_button.changeColorOnHover(mouse_pos,"MAGENTA")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if train_model_button.isHover(mouse_pos):
                    trainModel()

            exit_button.changeColorOnHover(mouse_pos,"MAGENTA")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.isHover(mouse_pos):
                    running = False
        
        screen.fill((0,0,0))
        draw_button(guess_button)
        draw_button(train_model_button)
        draw_button(exit_button)
        draw_text(main_menu_title)
        
        pygame.display.update() 
        clock.tick(60)

    pygame.quit()

def guessNumber():
    pass

def trainModel():

    data_json = "data.json"
    try:
        with open(data_json, "r", encoding="utf-8") as arquivo:
            number_list = json.load(arquivo)
    except:
        number_list = []
    
    screen.fill((0,0,0))
    drawing = {"isDrawing" : False, "isFirstRep" : True, "isAbleToDraw" : True}
    typing = False
    number = None
    running = True
    while running:

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            
            if event.type == QUIT:
                sys.exit()

            return_button.changeColorOnHover(mouse_pos, "MAGENTA")
            erase_button.changeColorOnHover(mouse_pos, "MAGENTA")
            trainDB_button.changeColorOnHover(mouse_pos, "MAGENTA")

            if not mouse_on_area(mouse_pos, drawing_area):
                drawing["isDrawing"] = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if mouse_on_area(mouse_pos, drawing_area):
                    drawing["isDrawing"] = True

                if mouse_on_area(mouse_pos, typing_area):
                    typing = True
                    typing_area.set_color("NOT_TOO_WHITE")
                else:
                    typing = False
                    typing_area.set_color("WHITE")
                
                if return_button.isHover(mouse_pos):
                    running = False

                if erase_button.isHover(mouse_pos):
                    screen.fill((0,0,0))
                    number = None
                    typing_text.set_text("")
                    drawing["isAbleToDraw"] = True

                if trainDB_button.isHover(mouse_pos):
                    if number is not None and addNumberToDataBase(data_json, number, number_list):
                        screen.fill((0,0,0))
                        number = None
                        typing_text.set_text("")
                        draw_text(added_to_db_text)
                        draw_text(press_erase_text)
                        draw_text(to_continue_text)
                        drawing["isAbleToDraw"] = False



            if event.type == pygame.MOUSEBUTTONUP:
                drawing["isDrawing"] = False
                drawing["isFirstRep"] = True

            if event.type == pygame.KEYDOWN and typing:

                if event.key == pygame.K_BACKSPACE:
                    number = None
                    typing_text.set_text("")
                else:
                    if event.unicode.isdigit():
                        number = event.unicode
                        typing_text.set_text(str(number))



        pygame.draw.line(screen, "WHITE", (drawing_area.get_width(), 0), (drawing_area.get_width(), screen_height), 3)

        #define o menor retangulo que cobre todos os botões da tela
        buttons_rect = [trainDB_button.get_x_pos(), trainDB_button.get_y_pos(), trainDB_button.get_x_pos()+trainDB_button.get_width(), (return_button.get_y_pos()+return_button.get_height())-trainDB_button.get_y_pos()]
        pygame.draw.rect(screen, "BLACK", buttons_rect)
        typing_area_rect = [typing_area.get_x_pos(), typing_area.get_y_pos(), typing_area.get_width(), typing_area.get_height()]
        pygame.draw.rect(screen, typing_area.get_color(), typing_area_rect)

        draw_button(return_button)
        draw_button(erase_button)
        draw_button(trainDB_button)
        draw_text(typing_text)

        if drawing["isDrawing"] and drawing["isAbleToDraw"]:
            pygame.draw.circle(screen, color_dict["DRAWING_COLOR"], mouse_pos, 2, 5)
            if not drawing["isFirstRep"]:
                pygame.draw.line(screen, color_dict["DRAWING_COLOR"], mouse_pos, mouse_last_pos, 5)
            mouse_last_pos = mouse_pos
            drawing["isFirstRep"] = False

        pygame.display.update() 
        clock.tick(60)


if __name__ == "__main__":
    main_menu()



