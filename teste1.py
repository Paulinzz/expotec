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

# Função de fade-in
def fade_in(tela, cor, largura, altura):
    fade_surface = pygame.Surface((largura, altura))
    fade_surface.fill(cor)
    for alpha in range(0, 255):
        fade_surface.set_alpha(alpha)
        tela.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(3)  # Controle da velocidade do fade

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

# Função para desenhar os botões do menu com hover
def desenhar_botoes_menu(tela, fonte, branca, preta, verde, vermelha, mouse_pos):
    draw_text('Menu Inicial', fonte, branca, tela, 300, 100)

    # Cores dos botões (muda quando o mouse está em cima)
    cor_jogar = branca if not pygame.Rect(300, 250, 200, 50).collidepoint(mouse_pos) else verde
    cor_ranking = branca if not pygame.Rect(300, 350, 200, 50).collidepoint(mouse_pos) else verde
    cor_sair = branca if not pygame.Rect(300, 450, 200, 50).collidepoint(mouse_pos) else vermelha

    # Desenha os botões
    button_jogar = pygame.Rect(300, 250, 200, 50)
    button_ranking = pygame.Rect(300, 350, 200, 50)
    button_sair = pygame.Rect(300, 450, 200, 50)

    pygame.draw.rect(tela, cor_jogar, button_jogar)
    pygame.draw.rect(tela, cor_ranking, button_ranking)
    pygame.draw.rect(tela, cor_sair, button_sair)

    draw_text('Jogar', fonte, preta, tela, 370, 260)
    draw_text('Ranking', fonte, preta, tela, 370, 360)
    draw_text('Sair', fonte, preta, tela, 370, 460)

    return button_jogar, button_ranking, button_sair,

def selecionar_controles():
    largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo = configurar_jogo()
    click = False
    controles_selecionados = 'setas'  # Padrão de controles
    controle_selecionado = False  # Controla se um controle já foi selecionado

    while True:
        tela.fill(preta)
        draw_text('Selecione seus controles:', fonte, branca, tela, 200, 100)

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

        if controle_selecionado:
            button_iniciar = pygame.Rect(300, 550, 200, 50)
            pygame.draw.rect(tela, verde, button_iniciar)
            draw_text('Iniciar Jogo', fonte, preta, tela, 340, 560)

        mx, my = pygame.mouse.get_pos()

        if button_wasd.collidepoint((mx, my)) and click:
            controles_selecionados = 'wasd'
            controle_selecionado = True  # Marca que o controle foi selecionado
        if button_setas.collidepoint((mx, my)) and click:
            controles_selecionados = 'setas'
            controle_selecionado = True  # Marca que o controle foi selecionado
        if button_voltar.collidepoint((mx, my)) and click:
            return None  # Retorna o controle selecionado
        
        if controle_selecionado and button_iniciar.collidepoint((mx,my)) and click:
            return controle_selecionado

        # Se o controle foi selecionado, exibe a mensagem "Controle Selecionado"
        if controle_selecionado:
            draw_text('Controle Selecionado', fonte, vermelha, tela, 200, 150)
            pygame.time.delay(5)

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
    fade_in(tela, preta, largura, altura)  # Efeito de fade-in na inicialização
    while True:
        mouse_pos = pygame.mouse.get_pos()
        tela.fill(preta)

        # Desenha o menu e os botões
        botoes = desenhar_botoes_menu(tela, fonte, branca, preta, verde, vermelha, mouse_pos)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        # Detecta cliques nos botões
        if click:
            if botoes[0].collidepoint(mouse_pos):
                jogador = inserir_nick(tela, fonte, branca, preta)
                controles_selecionados = selecionar_controles()
                rodar_jogo(largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo, jogador)
            elif botoes[1].collidepoint(mouse_pos):
                exibir_ranking()
            elif botoes[2].collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Funções do jogo da cobrinha (mantido conforme estava)
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
                elif controles_selecionados == 'wasd':
                    velocidade_x, velocidade_y = movimentar_wasd(evento.key, velocidade_x, velocidade_y, tamanho_quadrado)

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

    # Registrar a pontuação e exibir o ranking
    registrar_pontuacao(jogador, tamanho_cobra - 1)
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

# Função para registrar a pontuação
def registrar_pontuacao(jogador, pontuacao):
    with open('ranking.txt', 'a') as arq:
        arq.write(jogador + '\n')
        arq.write(str(pontuacao) + '\n')

def ler_e_ordenar_ranking():
    with open('ranking.txt') as arq:
        linhas = arq.readlines()

    ranking = []
    for i in range(0, len(linhas), 2):
        nome = linhas[i].strip()
        pontuacao = int(linhas[i + 1].strip())
        ranking.append([pontuacao, nome])

    # Ordena o ranking por pontuação em ordem decrescente
    return sorted(ranking, reverse=True)

# Função para exibir o ranking
def exibir_ranking():
    largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo = configurar_jogo()
    click = False

    while True:
        tela.fill(preta)
        draw_text('Ranking', fonte, branca, tela, 300, 100)

        # Chama a função para ler e ordenar o ranking
        ranking_ordenado = ler_e_ordenar_ranking()

        # Exibe os 7 melhores jogadores
        y_offset = 200
        for pontuacao, nome in ranking_ordenado[:7]:
            draw_text(f"{nome} - {pontuacao}", fonte, branca, tela, 300, y_offset)
            y_offset += 40

        # Botão para voltar ao menu
        mx, my = pygame.mouse.get_pos()
        button_voltar = pygame.Rect(300, 500, 200, 50)

        if button_voltar.collidepoint((mx, my)) and click:
            main_menu()

        pygame.draw.rect(tela, branca, button_voltar)
        draw_text('Voltar ao Menu', fonte, preta, tela, 300, 510)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        pygame.display.update()

# Inicializa o menu
main_menu()
