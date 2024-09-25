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

# Função para inserir o nome do jogador
def inserir_nick(tela, fonte, branca, preta):
    nick = ''
    inserindo = True
    while inserindo:
        tela.fill(preta)
        draw_text('Digite seu nome:', fonte, branca, tela, 300, 100)
        draw_text(nick, fonte, branca, tela, 300, 200)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Pressionar Enter para confirmar
                    if nick != '':
                        return nick
                elif event.key == pygame.K_BACKSPACE:
                    nick = nick[:-1]
                else:
                    nick += event.unicode

# Função para desenhar os botões do menu
def desenhar_botoes_menu(tela, fonte, branca, preta):
    tela.fill(preta)
    draw_text('Menu Inicial', fonte, branca, tela, 300, 100)

    # Botões
    button_1 = pygame.Rect(300, 250, 200, 50)
    button_2 = pygame.Rect(300, 350, 200, 50)
    button_3 = pygame.Rect(300, 450, 200, 50)
    button_controles = pygame.Rect(300, 550, 200, 50)
    
    pygame.draw.rect(tela, branca, button_1)
    pygame.draw.rect(tela, branca, button_2)
    pygame.draw.rect(tela, branca, button_3)
    pygame.draw.rect(tela, branca, button_controles)

    draw_text('Jogar', fonte, preta, tela, 370, 260)
    draw_text('Sair', fonte, preta, tela, 370, 360)
    draw_text('Ranking', fonte, preta, tela, 345, 460)
    draw_text('Controles', fonte, preta, tela, 345, 560)

    return button_1, button_2, button_3, button_controles

# Função para lidar com cliques do menu
def verificar_cliques_menu(mx, my, click, button_1, button_2, button_3, button_controles, tela, fonte, branca, preta):
    if button_1.collidepoint((mx, my)) and click:
        jogador = inserir_nick(tela, fonte, branca, preta)
        return 'play', jogador
    if button_2.collidepoint((mx, my)) and click:
        pygame.quit()
        sys.exit()
    if button_3.collidepoint((mx, my)) and click:
        return 'ranking', None
    if button_controles.collidepoint((mx, my)) and click:
        return 'controles', None
    return None, None

# Função para exibir a tela de seleção de controles
def selecionar_controles():
    largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo = configurar_jogo()
    click = False
    controles_selecionados = 'setas'  # Padrão de controles

    while True:
        tela.fill(preta)
        draw_text('Selecione seus controles:', fonte, branca, tela, 250, 100)

        # Botões de controle
        button_wasd = pygame.Rect(300, 250, 200, 50)
        button_setas = pygame.Rect(300, 350, 200, 50)
        button_voltar = pygame.Rect(300, 450, 200, 50)

        pygame.draw.rect(tela, branca, button_wasd)
        pygame.draw.rect(tela, branca, button_setas)
        pygame.draw.rect(tela, branca, button_voltar)

        draw_text('WASD', fonte, preta, tela, 370, 260)
        draw_text('Setas', fonte, preta, tela, 370, 360)
        draw_text('Voltar', fonte, preta, tela, 370, 460)

        mx, my = pygame.mouse.get_pos()

        if button_wasd.collidepoint((mx, my)) and click:
            controles_selecionados = 'wasd'
        if button_setas.collidepoint((mx, my)) and click:
            controles_selecionados = 'setas'
        if button_voltar.collidepoint((mx, my)) and click:
            return controles_selecionados

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        pygame.display.update()

# Função para exibir o menu inicial
def main_menu():
    largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo = configurar_jogo()
    click = False
    controles_selecionados = 'setas'  # Padrão de controles

    while True:
        button_1, button_2, button_3, button_controles = desenhar_botoes_menu(tela, fonte, branca, preta)

        mx, my = pygame.mouse.get_pos()
        acao, jogador = verificar_cliques_menu(mx, my, click, button_1, button_2, button_3, button_controles, tela, fonte, branca, preta)

        if acao == 'play':
            rodar_jogo(largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo, jogador, controles_selecionados)
        elif acao == 'ranking':
            exibir_ranking()
        elif acao == 'controles':
            controles_selecionados = selecionar_controles()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        pygame.display.update()

# Função para rodar o jogo com base na escolha de controles
def rodar_jogo(largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo, jogador, controles_selecionados):
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
                if controles_selecionados == 'setas':
                    velocidade_x, velocidade_y = movimentar_setas(evento.key, velocidade_x, velocidade_y, tamanho_quadrado)
                else:
                    velocidade_x, velocidade_y = movimentar_wasd(evento.key, velocidade_x, velocidade_y, tamanho_quadrado)

        x, y = x + velocidade_x, y + velocidade_y
        fim_jogo = verificar_fim_jogo(x, y, largura, altura, pixels)

        desenhar_cobra(tela, verde, pixels, tamanho_cobra, x, y)
        comida_x, comida_y, tamanho_cobra = verificar_colisao_comida(x, y, comida_x, comida_y, tamanho_cobra, tamanho_quadrado, largura, altura, tela, vermelha)

        pygame.display.update()
        relogio.tick(velocidade_jogo)

    pygame.quit()
    sys.exit()

# Funções auxiliares para movimentação com WASD e setas
def movimentar_setas(tecla, velocidade_x, velocidade_y, tamanho_quadrado):
    if tecla == pygame.K_LEFT and velocidade_x == 0:
        return -tamanho_quadrado, 0
    if tecla == pygame.K_RIGHT and velocidade_x == 0:
        return tamanho_quadrado, 0
    if tecla == pygame.K_UP and velocidade_y == 0:
        return 0, -tamanho_quadrado
    if tecla == pygame.K_DOWN and velocidade_y == 0:
        return 0, tamanho_quadrado
    return velocidade_x, velocidade_y

def movimentar_wasd(tecla, velocidade_x, velocidade_y, tamanho_quadrado):
    if tecla == pygame.K_a and velocidade_x == 0:
        return -tamanho_quadrado, 0
    if tecla == pygame.K_d and velocidade_x == 0:
        return tamanho_quadrado, 0
    if tecla == pygame.K_w and velocidade_y == 0:
        return 0, -tamanho_quadrado
    if tecla == pygame.K_s and velocidade_y == 0:
        return 0, tamanho_quadrado
    return velocidade_x, velocidade_y

# Função principal do jogo
def main():
    main_menu()

if __name__ == "__main__":
    main()
