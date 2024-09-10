# Configurações iniciais
import pygame
import random
import sys

pygame.init()
pygame.display.set_caption("Snake The Game")

largura, altura = 1560, 760
# largura, altura = 800, 600  # opção 2 

tela = pygame.display.set_mode((largura, altura))

relogio = pygame.time.Clock()

# Cores
preta = (0, 0, 0)
branca = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)

# Parâmetros da cobrinha
tamanho_quadrado = 20
velocidade_jogo = 15

def exibir_mensagem(texto, tamanho_fonte, cor, posicao):
    fonte = pygame.font.SysFont("Helvetica", tamanho_fonte)
    mensagem = fonte.render(texto, True, cor)
    tela.blit(mensagem, posicao)

def tela_mensagem_inicial():
    """Exibe uma mensagem antes do menu inicial"""
    tela.fill(preta)
    exibir_mensagem("Bem-vindo ao Snake The Game!", 50, branca, (largura // 4, altura // 2 - 50))
    exibir_mensagem("Pressione qualquer tecla para continuar...", 35, branca, (largura // 4, altura // 2 + 50))
    pygame.display.update()
    
    # Espera o jogador pressionar qualquer tecla
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                return

def exibir_menu_inicial():
    """Exibe o menu inicial para iniciar o jogo"""
    tela.fill(preta)
    exibir_mensagem("Menu Inicial", 50, branca, (largura // 3, altura // 3 - 50))
    exibir_mensagem("1. Jogar", 35, verde, (largura // 3, altura // 3 + 50))
    exibir_mensagem("2. Sair", 35, verde, (largura // 3, altura // 3 + 100))
    pygame.display.update()

    # Espera o jogador selecionar a opção do menu
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return  # Inicia o jogo
                if evento.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

def gerar_comida(pixels):
    """Gera a posição da comida em locais que não estão ocupados pela cobra"""
    while True:
        comida_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
        comida_y = round(random.randrange(0, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
        if [comida_x, comida_y] not in pixels:
            return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render(f"Pontos: {pontuacao}", True, vermelha)
    tela.blit(texto, [1, 1])

def selecionar_velocidade(tecla, velocidade_x, velocidade_y):
    """Seleciona a nova velocidade da cobra, impedindo movimento reverso"""
    if tecla == pygame.K_DOWN and velocidade_y == 0:
        return 0, tamanho_quadrado
    elif tecla == pygame.K_UP and velocidade_y == 0:
        return 0, -tamanho_quadrado
    elif tecla == pygame.K_RIGHT and velocidade_x == 0:
        return tamanho_quadrado, 0
    elif tecla == pygame.K_LEFT and velocidade_x == 0:
        return -tamanho_quadrado, 0
    return velocidade_x, velocidade_y  # Mantém a direção atual

def ignorar_tecla_nao_seta(tecla):
    """Ignora teclas que não sejam setas de direção"""
    return tecla not in [pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT]

def rodar_jogo():
    fim_jogo = False
    x = largura / 2
    y = altura / 2
    velocidade_x = tamanho_quadrado  # Inicia movendo para a direita
    velocidade_y = 0
    tamanho_cobra = 1
    pixels = []
    comida_x, comida_y = gerar_comida(pixels)

    while not fim_jogo:
        tela.fill(preta)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                if ignorar_tecla_nao_seta(evento.key):
                    continue
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key, velocidade_x, velocidade_y)

        # Atualizar a posição da cobra
        x += velocidade_x
        y += velocidade_y

        # Checa se a cobra saiu dos limites da tela e teletransporta para o lado oposto
        if x < 0:
            x = largura - tamanho_quadrado
        elif x >= largura:
            x = 0
        if y < 0:
            y = altura - tamanho_quadrado
        elif y >= altura:
            y = 0

        # Adiciona a nova posição da cabeça da cobra
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        # Verifica se a cobra bateu no próprio corpo
        if [x, y] in pixels[:-1]:
            fim_jogo = True

        # Desenha os elementos na tela
        desenhar_comida(tamanho_quadrado, comida_x, comida_y)
        desenhar_cobra(tamanho_quadrado, pixels)
        desenhar_pontuacao(tamanho_cobra - 1)

        # Atualiza a tela
        pygame.display.update()

        # Verifica se a cobra comeu a comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida(pixels)

        # Controle da velocidade do jogo
        relogio.tick(velocidade_jogo)

# Exibe a mensagem inicial e o menu antes de iniciar o jogo
tela_mensagem_inicial()
exibir_menu_inicial()
rodar_jogo()
pygame.quit()
