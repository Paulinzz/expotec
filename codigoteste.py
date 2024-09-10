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
    fim_jogo, x, y = False, largura / 2, altura / 2
    velocidade_x, velocidade_y, tamanho_cobra = tamanho_quadrado, 0, 1
    pixels, comida_x, comida_y = [], *gerar_comida(pixels) #erro  aqui

    while not fim_jogo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            if evento.type == pygame.KEYDOWN and not ignorar_tecla_nao_seta(evento.key):
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key, velocidade_x, velocidade_y)

        x, y = (x + velocidade_x) % largura, (y + velocidade_y) % altura
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]
        fim_jogo = [x, y] in pixels[:-1]

        if [x, y] == [comida_x, comida_y]:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida(pixels)

        tela.fill(preta)
        desenhar_comida(tamanho_quadrado, comida_x, comida_y)
        desenhar_cobra(tamanho_quadrado, pixels)
        desenhar_pontuacao(tamanho_cobra - 1)
        pygame.display.update()
        relogio.tick(velocidade_jogo)



# Exibe a mensagem inicial e o menu antes de iniciar o jogo
tela_mensagem_inicial()
exibir_menu_inicial()
rodar_jogo()
pygame.quit()
