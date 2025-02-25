import cv2
import numpy as np
import pygame
from pygame.locals import *

#define as constantes referentes às cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (200, 0, 100)

#define as informações da tela
screen_width = 640
screen_height = 480

#inicia a tela em que o programa será executado
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height)) #criacao da tela
clock = pygame.time.Clock()
pygame.display.set_caption("Number Detector") #titulo da janela

#define as informações do botão 'guess number'
button_guess_number_width = 220
button_guess_number_height = 50
button_guess_number_X = screen_width//2 - button_guess_number_width//2
button_guess_number_Y = (screen_height//2)-button_guess_number_height
button_guess_number_border = 5
button_guess_number_info = [button_guess_number_X, button_guess_number_Y, button_guess_number_width, button_guess_number_height, "GUESS NUMBER", WHITE, button_guess_number_border]

#define as informações do botão 'train model'
button_train_model_width = 220
button_train_model_height = 50
button_train_model_X = button_guess_number_X
button_train_model_Y = button_guess_number_Y + button_guess_number_height + 10
button_train_model_border = 5
button_train_model_info = [button_train_model_X, button_train_model_Y, button_train_model_width, button_train_model_height, "TRAIN MODEL", WHITE, button_train_model_border]

#define as informações do botão 'exit'
button_exit_width = 220
button_exit_height = 50
button_exit_X = button_guess_number_X
button_exit_Y = button_train_model_Y + button_train_model_height + 10
button_exit_border = 5
button_exit_info = [button_exit_X, button_exit_Y, button_exit_width, button_exit_height, "EXIT", WHITE, button_exit_border]

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
def draw_button(button_info):

    rect = tuple(button_info[0:4])
    pygame.draw.rect(screen, button_info[5], rect, button_info[6])

    text_content = button_info[4]
    text_X = button_info[0]+(button_info[2]//2)
    text_Y = button_info[1]+(button_info[3]//2)
    text_colour = button_info[5]
    text_info = [text_content, text_X, text_Y, text_colour]

    if button_info[4] != "":
        draw_text(text_info)

#função que exibe o menu principal da aplicação
def mainMenu():

    running = True
    while running:

        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                running = False
            
            if mouse_on_area(mouse_pos, button_guess_number_info[0:4]):
                button_guess_number_info[5] = MAGENTA
                if event.type == pygame.MOUSEBUTTONDOWN:
                    guessNumberScreen()
            else:
                button_guess_number_info[5] = WHITE
                
            if mouse_on_area(mouse_pos, button_train_model_info[0:4]):
                button_train_model_info[5] = MAGENTA
                if event.type == pygame.MOUSEBUTTONDOWN:
                    trainModelScreen()
            else:
                button_train_model_info[5] = WHITE

            if mouse_on_area(mouse_pos, button_exit_info[0:4]):
                button_exit_info[5] = MAGENTA
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
            else:
                button_exit_info[5] = WHITE
        
        screen.fill(BLACK)
        draw_button(button_guess_number_info)
        draw_button(button_train_model_info)
        draw_button(button_exit_info)
        
        pygame.display.update() 
        clock.tick(60)

def guessNumberScreen():
    pass

def trainModelScreen():
    pass

mainMenu()