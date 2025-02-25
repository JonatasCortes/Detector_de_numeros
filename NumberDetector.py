from time import process_time_ns

import cv2
import numpy as np
import pygame
from pygame.locals import *
from Detector_de_numeros.Lib.Schemas.DefaultButton import DefaultButton

#define as constantes referentes às cores

#define as informações da tela
screen_width = 640
screen_height = 480

#inicia a tela em que o programa será executado
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height)) #criacao da tela
clock = pygame.time.Clock()
pygame.display.set_caption("Number Detector") #titulo da janela

#define as informações do botão 'guess number'

guess_button = DefaultButton(height=50,width=220,border=5,text="GUESS NUMBER",colour="WHITE")
guess_button.set_x_pos((screen_width//2- guess_button.get_width()//2))
guess_button.set_y_pos((screen_height//2)-guess_button.get_height())

#define as informações do botão 'train model'

train_model_button = DefaultButton(width=220, height=50,border= 5, colour="WHITE", text= "TRAIN MODEL")
train_model_button.set_x_pos(guess_button.get_x_pos())
train_model_button.set_y_pos(guess_button.get_y_pos() + guess_button.get_height() + 10)

#define as informações do botão 'exit'

exit_button = DefaultButton(width=220, height=50,border= 5, colour="WHITE", text= "EXIT")
exit_button.set_x_pos(guess_button.get_x_pos())
exit_button.set_y_pos(train_model_button.get_y_pos()+ train_model_button.get_height() + 10)



#verifica se o mouse esta sobre uma certa area
def mouse_on_area(mouse_pos, area_info):
    if area_info[0] <= mouse_pos[0] <= area_info[0] + area_info[2] and area_info[1] <= mouse_pos[1] <= area_info[1] + area_info[3]:
        return True
    else:
        return False

#função que exibe um texto na tela
def draw_text(text_info):

    font = pygame.font.Font(None, 36)

    text_surface = font.render(text_info[0], True, text_info[3])
    text_rect = text_surface.get_rect(center=(text_info[1], text_info[2]))

    screen.blit(text_surface, text_rect)

#função que exibe um botão na tela
def draw_button(button_info:DefaultButton):

    rect = button_info.get_x_pos(),button_info.get_y_pos(),button_info.get_width(),button_info.get_height()
    pygame.draw.rect(screen, button_info.get_colour(), rect, button_info.get_border())

    text_content = button_info.get_text()
    text_x = button_info.get_x_pos()+(button_info.get_width()//2)
    text_y = button_info.get_y_pos()+(button_info.get_height()//2)
    text_colour = button_info.get_colour()
    text_info = [text_content, text_x, text_y, text_colour]

    if button_info.get_text() != "":
        draw_text(text_info)




#função que exibe o menu principal da aplicação
def main_menu():

    running = True
    while running:

        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                running = False



            guess_button.onHover(mouse_pos,"MAGENTA")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if guess_button.isHover(mouse_pos):
                    guessNumberScreen()
                    print("hello")

            train_model_button.onHover(mouse_pos,"MAGENTA")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if train_model_button.isHover(mouse_pos):
                    guessNumberScreen()
                    print("hello")

            exit_button.onHover(mouse_pos,"MAGENTA")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.isHover(mouse_pos):
                    guessNumberScreen()
                    running = False


        
        screen.fill((0,0,0))
        draw_button(guess_button)
        draw_button(train_model_button)
        draw_button(exit_button)
        
        pygame.display.update() 
        clock.tick(60)

def guessNumberScreen():
    pass

def trainModelScreen():
    pass

if __name__ == "__main__":
    main_menu()



