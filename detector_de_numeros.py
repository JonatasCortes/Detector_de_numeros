import cv2
import numpy as np
import pygame
from pygame.locals import *

def mainScreen():
    pygame.init()

    #informacoes da tela
    screen_width = 640 #largura
    screen_height = 480 #altura
    screen = pygame.display.set_mode((screen_width, screen_height)) #criacao da tela
    clock = pygame.time.Clock()

    pygame.display.set_caption("Identificador de numeros do balacobaco") #titulo da janela

    #cores
    COLOUR_DRAW = (250, 250, 250)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    MAGENTA = (200, 0, 100)
    BLACK = (0, 0, 0)

    #informacoes relacionadas ao desenho
    able_to_draw = True
    drawing = False
    pencil_width = 5

    #informacoes do botao GUESS
    button_guess_colour = WHITE
    button_guess_x = 400
    button_guess_y = 400
    button_guess_width = 220
    button_guess_height = 50

    #informacoes do botao ERASE
    button_erase_colour = WHITE
    button_erase_x = button_guess_x
    button_erase_y = button_guess_y - 60
    button_erase_width = button_guess_width
    button_erase_height = button_guess_height

    #informacoes relacionadas ao texto "WHITES"
    text_whites_colour = WHITE
    text_whites_x = button_erase_x+50
    text_whites_y = button_erase_y-50

    #informacoes relacionadas ao texto "BLACKS"
    text_blacks_colour = WHITE
    text_blacks_x = text_whites_x
    text_blacks_y = text_whites_y-30

    #informacoes sobre a linha que divide a tela
    dividing_line_colour = WHITE
    dividing_line_x = 385
    dividing_line_width = 5

    #informacoes sobre os pixels desenhados
    num_white_pixels, num_black_pixels = 0, 0
    min_x, min_y, max_x, max_y = None, None, None, None

    #funcao que gera um texto na tela
    def draw_text(text, text_x, text_y, text_color):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        screen.blit(text_surface, text_rect)

    #funcao que gera um botao na tela
    def draw_button(screen, color, text_color, x, y, width, height, text="", rect_width = 5):
        pygame.draw.rect(screen, color, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x+rect_width, y+rect_width, width-rect_width*2, height-rect_width*2))

        if text != "":
            draw_text(text, x + width // 2, y + height // 2, text_color)

    #funcao que muda a cor do botao quando o mouse esta por cima
    def change_colour_on_hoover(button_x, button_y, button_width, button_height, new_colour, default_color = WHITE):
        if mouse_on_area(mouse_pos, button_x, button_y, button_width, button_height):
            return new_colour
        else:
            return default_color
    
    #verifica se o mouse esta sobre uma certa area
    def mouse_on_area(mouse_pos, area_x, area_y, area_width, area_height):
        if area_x <= mouse_pos[0] <= area_x + area_width and area_y <= mouse_pos[1] <= area_y + area_height:
            return True
        else:
            return False

    #loop principal da tela
    running = True
    while running:

        mouse_pos = pygame.mouse.get_pos() #armazena a posicao do mouse em uma variavel

        #loop que verifica eventos 
        for event in pygame.event.get():

            #verifica se o usuario fechou a janela e entao encerra a execussao do loop principal
            if event.type == QUIT:
                running = False
            
            #impede que o usuario desenhe apos a linha de divisao da tela
            if mouse_on_area(mouse_pos, dividing_line_x, 0, screen_width-dividing_line_x, screen_height):
                drawing = False

            #verifica se o botao esquerdo do mouse esta pressionado
            first_repetition = True
            if event.type == pygame.MOUSEBUTTONDOWN:

                #verifica se o usuario esta na regiao correta para desenho
                if first_repetition and able_to_draw and mouse_pos[0] < dividing_line_x:
                    pygame.draw.rect(screen, BLACK, (dividing_line_x, 0, screen_width-dividing_line_x, screen_height))#remove os dados do desenho anterior da tela
                    first_repetition = False #faz com que esse codigo seja executado apenas uma vez por desenho
                    drawing = True #avisa o programa de que o usuario esta desenhando
                    counter=0 #zera a contagem da repeticao do programa

                #define as consequencias do botao ERASE
                if mouse_on_area(mouse_pos, button_erase_x, button_erase_y, button_erase_width, button_erase_height):
                    able_to_draw = True #permite que o usuario volte a desenhar
                    screen.fill(BLACK) #apaga as informacoes do numero anterior
                
                #define as consequencias do botao GUESS
                if mouse_on_area(mouse_pos, button_guess_x, button_guess_y, button_guess_width, button_guess_height):
                    
                    # Captura a tela como uma superfície
                    print_screen = pygame.surfarray.array3d(screen)

                    # Converte de RGB (Pygame) para BGR (OpenCV)
                    print_screen = np.rot90(print_screen)  #Corrige orientação
                    print_screen = print_screen[::-1] #Corrige a orientacao 2
                    print_screen = cv2.cvtColor(print_screen, cv2.COLOR_RGB2BGR) #Corrige a paleta de cores

                    #declaracao das variaveis referentes aos pixels da area desenhada
                    pixels = []
                    num_white_pixels, num_black_pixels = 0, 0
                    min_x, min_y, max_x, max_y = None, None, None, None

                    #extrai as coordenadas de todos os pixels desenhados
                    #a funcao np.argwhere() retorna uma matriz com os indices onde as condicoes de seu parametro sao verdadeiras em print_screen
                    #eu ainda nao entendi pra que serve a condicao que vem depois do '&', mas sem ela o codigo nao funciona, obrigado chatGPT
                    pixels = np.argwhere((print_screen == COLOUR_DRAW).all(axis=2) & (np.arange(print_screen.shape[1])[None, :] < dividing_line_x))
                    
                    try:
                        #percorre a matriz dos indices dos pixels desenhados e retorna as coordenadas de suas extremidades
                        min_y, min_x = pixels.min(axis=0)
                        max_y, max_x = pixels.max(axis=0)

                        #filtra os pixels da tela e gera uma matriz onde os pixels desenhados sao 1 e os pretos sao 0
                        drawn_screen = np.where((print_screen == COLOUR_DRAW).all(axis=2), 1, 0)
                        drawn_region = drawn_screen[min_y:max_y+1, min_x:max_x+1]#restringe a tela ao menor retangulo capaz de cobrir todos os pixels desenhados

                        #conta o numero de pixels desenhados e nao desenhados na area delimitada
                        num_white_pixels = np.sum(drawn_region == 1)
                        num_black_pixels = np.sum(drawn_region == 0)
                        number_density = num_white_pixels/(num_white_pixels+num_black_pixels) #estabelece a densidade da area
                        print(number_density)
                    
                    #ocorre em caso de o usuario clicar no botao GUESS sem ter desenhado nada
                    except:
                        able_to_draw = False #impede que o usuario volte a desenhar sem que leia a mensagem

                        reference_x = ((screen_width-dividing_line_x)//2)+70 #define a coordenada x da mensagem
                        reference_y = screen_height//2 #define a coordenada y da mensagem

                        #imprime a mensagem na tela do uduario
                        draw_text("ESCREVA UM NÚMERO!", reference_x, reference_y-30, MAGENTA)
                        draw_text("APERTE 'ERASE'", reference_x, reference_y, MAGENTA)
                        draw_text("PARA CONTINUAR", reference_x, reference_y+30, MAGENTA)

                    #imprime a quantidade de pixels brancos e pretos na regiao desenhada
                    draw_text(f"{num_white_pixels}", text_whites_x+100, text_whites_y, text_whites_colour)
                    draw_text(f"{num_black_pixels}", text_blacks_x+100, text_blacks_y, text_blacks_colour)

            #imprime os botoes na tela
            button_guess_colour = change_colour_on_hoover(button_guess_x, button_guess_y, button_guess_width, button_guess_height, MAGENTA, WHITE)
            button_erase_colour = change_colour_on_hoover(button_erase_x, button_erase_y, button_erase_width, button_erase_height, MAGENTA, WHITE)

            #verifica se o botao esquerdo do mouse nao esta sendo pressionado
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False #avisa o programa de que o usuario nao esta mais desenhando

        #verifica se o usuario esta desenhando
        if drawing:
            pygame.draw.circle(screen, COLOUR_DRAW, mouse_pos, pencil_width/2, pencil_width)#faz com que as consecutivas linhas desenhadas sejam conectadas por pontos
            if counter != 0:
                #verifica se nao eh a primeira repeticao e entao desenha linhas entre as consecutivas posicoes verificadas do mouse
                pygame.draw.line(screen, COLOUR_DRAW, mouse_pos, mouse_last_position, pencil_width)
                
            mouse_last_position = mouse_pos #atualiza a posicao anterior do mouse
            counter += 1 #aumenta a contagem de repeticoes

        #imprime os botoes na tela do usuario
        draw_button(screen, button_guess_colour, button_guess_colour, button_guess_x, button_guess_y, button_guess_width, button_guess_height, "GUESS NUMBER")
        draw_button(screen, button_erase_colour, button_erase_colour, button_erase_x, button_erase_y, button_erase_width, button_erase_height, "ERASE")
        #imprime os textos na tela do usuario
        draw_text("WHITES:", text_whites_x, text_whites_y, text_whites_colour)
        draw_text("BLACKS:", text_blacks_x, text_blacks_y, text_blacks_colour)

        #desenha a linha que divide a tela entre a area de desenho e o display de informacoes
        pygame.draw.line(screen, dividing_line_colour, (dividing_line_x, 0), (dividing_line_x, screen_height), dividing_line_width)

        #atualiza os frames e limita a taxa de atualizacao para 60fps
        pygame.display.update() 
        clock.tick(60)      

    #encerra a aplicacao
    pygame.quit()

mainScreen()