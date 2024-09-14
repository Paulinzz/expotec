import pygame
import random
import sys

# Inicializando o Pygame
pygame.init()

# Função para configurar as variáveis principais e retornar seus valores
def configurar_jogo():
    largura, altura = 800, 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Snake The Game')
    fonte = pygame.font.SysFont('Arial', 40)
    icone = pygame.image.load("OIP.jpeg") 
    pygame.display.set_icon(icone)
    
    # Definindo cores
    branca = (255, 255, 255)
    preta = (0, 0, 0)
    verde = (0, 255, 0)
    vermelha = (255, 0, 0)

    # Parâmetros do jogo
    tamanho_quadrado = 20
    velocidade_jogo = 15

    return largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo

# Função para exibir texto na tela
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Função para exibir o menu inicial
def main_menu():
    largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo = configurar_jogo()
    click = False
    while True:
        tela.fill(preta)
        draw_text('Menu Inicial', fonte, branca, tela, 300, 100)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(300, 250, 200, 50)
        button_2 = pygame.Rect(300, 350, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                rodar_jogo(largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo)
        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(tela, branca, button_1)
        pygame.draw.rect(tela, branca, button_2)

        draw_text('Jogar', fonte, preta, tela, 370, 260)
        draw_text('Sair', fonte, preta, tela, 370, 360)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

# Funções do jogo da cobrinha
def rodar_jogo(largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo):
    relogio = pygame.time.Clock()
    fim_jogo, x, y = False, largura / 2, altura / 2
    velocidade_x, velocidade_y = tamanho_quadrado, 0
    tamanho_cobra, pixels = 1, []
    comida_x, comida_y = gerar_comida(pixels, largura, altura, tamanho_quadrado)

    while not fim_jogo:
        tela.fill(preta)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key, velocidade_x, velocidade_y, tamanho_quadrado)

        x, y = atualizar_cobra(x, y, velocidade_x, velocidade_y, tamanho_cobra, pixels)
        if verificar_colisoes(x, y, largura, altura, pixels):
            fim_jogo = True

        desenhar_comida(tela, verde, tamanho_quadrado, comida_x, comida_y)
        desenhar_cobra(tela, branca, tamanho_quadrado, pixels)
        desenhar_pontuacao(tela, vermelha, tamanho_cobra - 1, fonte)

        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida(pixels, largura, altura, tamanho_quadrado)

        pygame.display.update()
        relogio.tick(velocidade_jogo)

    # Retorna ao menu após o jogo terminar
    main_menu()

def gerar_comida(pixels, largura, altura, tamanho_quadrado):
    while True:
        comida_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
        comida_y = round(random.randrange(0, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
        if [comida_x, comida_y] not in pixels:
            return comida_x, comida_y

def desenhar_comida(tela, verde, tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tela, branca, tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(tela, vermelha, pontuacao, fonte):
    texto = fonte.render(f"Pontos: {pontuacao}", True, vermelha)
    tela.blit(texto, [1, 1])

def selecionar_velocidade(tecla, velocidade_x, velocidade_y, tamanho_quadrado):
    if tecla == pygame.K_DOWN and velocidade_y == 0:
        return 0, tamanho_quadrado
    elif tecla == pygame.K_UP and velocidade_y == 0:
        return 0, -tamanho_quadrado
    elif tecla == pygame.K_RIGHT and velocidade_x == 0:
        return tamanho_quadrado, 0
    elif tecla == pygame.K_LEFT and velocidade_x == 0:
        return -tamanho_quadrado, 0
    return velocidade_x, velocidade_y  # Mantém a direção atual

def atualizar_cobra(x, y, velocidade_x, velocidade_y, tamanho_cobra, pixels):
    x += velocidade_x
    y += velocidade_y
    pixels.append([x, y])
    if len(pixels) > tamanho_cobra:
        del pixels[0]
    return x, y

def verificar_colisoes(x, y, largura, altura, pixels):
    if x < 0 or x >= largura or y < 0 or y >= altura or [x, y] in pixels[:-1]:
        return True
    return False

# Inicializa o menu
main_menu()
