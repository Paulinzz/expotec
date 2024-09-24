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
    fim_jogo = False
    pontuação = 0

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

    if fim_jogo:
        nome = input("Digite seu nome: ")
        salvar_pontuação(nome,pontuação)
        pontuação = desenhar_pontuacao
    


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

def salvar_pontuação(nome, pontuação):
    with open("ranking.txt", "a") as arquvio:
        arquvio.write(f"{nome}/{pontuação}")

def carregar_ranking():
    ranking = []
    try:
        with open("ranking.txt", "r") as arquivo:
            for linha in arquivo.readlines():
                nome, pontuação = linha.strip().split(":")
                ranking.append((nome, int(pontuação)))
        ranking.sort(key=lambda x: x[1], reverse=True)
    except FileNotFoundError:
        pass
    return ranking

def atualizar_pontuacao(nome, nova_pontuacao):
    ranking = carregar_ranking()  # Carrega o ranking atual
    jogador_existente = False

    # Verifica se o jogador já está no ranking
    for i, (jogador, pontuacao) in enumerate(ranking):
        if jogador == nome:
            jogador_existente = True
            if nova_pontuacao > pontuacao:  # Atualiza se a nova pontuação for maior
                ranking[i] = (nome, nova_pontuacao)
            break

    # Se o jogador não está no ranking, adiciona a nova pontuação
    if not jogador_existente:
        ranking.append((nome, nova_pontuacao))

    # Reordena o ranking
    ranking.sort(key=lambda x: x[1], reverse=True)

    # Salva o ranking atualizado de volta no arquivo
    with open('ranking.txt', 'w') as arquivo:
        for jogador, pontuacao in ranking:
            arquivo.write(f'{jogador},{pontuacao}\n')


def exibir_ranking(tela, fonte):
    tela.fill(0,0,0)
    ranking = carregar_ranking()
    
    if not ranking:
        draw_text("Nenhum ranking foi achado...", fonte, (255,255,255), tela, (100,100))
    else:
        draw_text("ranking", fonte, (255,255,255), tela, (300, 50 ))
        for i,(nome,pontuanção) in enumerate(ranking[:5]):
            texto = (f"{i+1}. {nome} - {pontuanção}pontos")
            draw_text(texto, fonte, (255,255,255), tela, (100, 100 + i * 50 ))
    pygame.display.update()

# Inicializa o menu
main_menu()
