import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Menu Inicial')


white = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.SysFont('Arial', 40)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        screen.fill(black)
        draw_text('Menu Inicial', font, white, screen, 300, 100)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(300, 250, 200, 50)
        button_2 = pygame.Rect(300, 350, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, white, button_1)
        pygame.draw.rect(screen, white, button_2)

        draw_text('Jogar', font, black, screen, 370, 260)
        draw_text('Sair', font, black, screen, 370, 360)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(black)
        draw_text('Jogo em andamento...', font, white, screen, 300, 300)
        pygame.display.update()

main_menu()
