import pygame
import random
import sys

# Inicializando o Pygame
pygame.init()

# Inicialização do Som
pygame.mixer.init()  

# Função para configurar as variáveis principais e retornar seus valores
def configurar_jogo():
    largura, altura = 800, 600 # defini a largura e altura (resolução).
    tela = pygame.display.set_mode((largura, altura)) # cria a janela para apresentar do game.
    pygame.display.set_caption('Snake The Game') # Nome para essa janela, escrito no canto superior esquerdo.
    fonte = pygame.font.SysFont('Arial', 40) # A fonte definida para o jogo
    icone = pygame.image.load("OIP.jpeg") # Icone representado no canto superior esquerdo, ao lado do nome.
    pygame.display.set_icon(icone) # representação do icone na janela.
    
    # Definindo cores
    branca = (255, 255, 255) # cor branca.
    preta = (0, 0, 0) # cor preta.
    verde = (0, 255, 0) # cor verde.
    vermelha = (255, 0, 0) # cor vermelha.

    # Parâmetros do jogo
    tamanho_quadrado = 20 # tamanho do quadrado, da cobrinha ou da comida.
    velocidade_jogo = 15 # velocidade ao qual a cobrinha se mover .

    '''retorno de todos os parâmetros'''
    return largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo 

# Função para exibir texto na tela
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

'''função para o famoso "fade-in "'''
def aparecimento(tela, cor, largura, altura):
    fade_surface = pygame.Surface((largura, altura))
    fade_surface.fill(cor)
    for alpha in range(0, 255):
        fade_surface.set_alpha(alpha)
        tela.blit(fade_surface, (0, 0))
        pygame.display.update() # atualização da tela para mostra-se o efeito.
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

    # crio um laço para verificar a "nick", enquanto ela tiver vazia, não é aceita, para a inciação do game.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # se houve um alt+f4 ou fecha a janela.
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
def desenhar_botoes_menu(tela, fonte, branca, preta, verde, vermelha):
    tela.fill(preta)
    draw_text('Menu Inicial', fonte, branca, tela, 300, 100)

    mx, my = pygame.mouse.get_pos()
   

    # Cores dos botões ao passar o mouse
    '''as cores servem para que quando passar o mouse por cima dos botões ele apareçam cores como verdes na maioria das vezes
    ou vermelha para o botão de sair'''
    cor_jogar = vermelha if pygame.Rect(300, 250, 200, 50).collidepoint(mx, my) else branca
    cor_controle = vermelha if pygame.Rect(300, 350, 200, 50).collidepoint(mx, my) else branca
    cor_ranking = vermelha if pygame.Rect(300, 450, 200, 50).collidepoint(mx, my) else branca
    cor_sair = verde if pygame.Rect(300, 550, 200, 50).collidepoint(mx, my) else branca

    # Botões
    '''definido a localização do eixo x,y e seu tamanho'''
    button_1 = pygame.Rect(300, 250, 200, 50)
    button_controles = pygame.Rect(300, 350, 200, 50)
    button_ranking = pygame.Rect(300, 450, 200, 50)
    button_sair = pygame.Rect(300, 550, 200, 50)
    
    pygame.draw.rect(tela, cor_jogar, button_1)
    pygame.draw.rect(tela, cor_controle, button_controles)
    pygame.draw.rect(tela, cor_ranking, button_ranking)
    pygame.draw.rect(tela, cor_sair, button_sair)

    '''escrevendo dentro dos botões'''
    draw_text('Jogar', fonte, preta, tela, 370, 260)
    draw_text('Controles', fonte, preta, tela, 345, 360)
    draw_text('Ranking', fonte, preta, tela, 345, 460)
    draw_text('Sair', fonte, preta, tela, 370, 560)

    return button_1, button_sair, button_ranking, button_controles

# Função para lidar com cliques do menu
def verificar_cliques_menu(mx, my, click, button_1, button_sair, button_ranking, button_controles, tela, fonte, branca, preta):
     # som para o click do mouse, quando selecionar alguma opção do menu.
    som_click = pygame.mixer.Sound('click.mp3')

    if button_1.collidepoint((mx, my)) and click:
        som_click.play() 
        jogador = inserir_nick(tela, fonte, branca, preta)
        som_click.play()
        return 'play', jogador
    if button_controles.collidepoint((mx, my)) and click:
        som_click.play()
        return 'controles', None 
    if button_ranking.collidepoint((mx, my)) and click:
        som_click.play()
        return 'ranking', None
    if button_sair.collidepoint((mx, my)) and click:
        pygame.quit()
        sys.exit() 
    return None, None

'''função responsável por desenhar os botões e nomes do menu de controle.'''
def desenhar_controles_menu(tela, fonte, branca, preta):
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

    return button_wasd, button_setas, button_voltar

'''função para definir o controle que o usuário queria utilizar.'''
def selecionar_controles():
    largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo = configurar_jogo()
    click = False
    controles_selecionados = 'setas'  # Padrão  pre-setado de controles
    controle_selecionado = False  # Controla se um controle já foi selecionado

    while True:
        button_wasd, button_setas, button_voltar = desenhar_controles_menu(tela, fonte, branca, preta)

        mx, my = pygame.mouse.get_pos()

        if button_wasd.collidepoint((mx, my)) and click:
            controles_selecionados = 'wasd'
            controle_selecionado = True  # Marca que o controle foi selecionado
        if button_setas.collidepoint((mx, my)) and click:
            controles_selecionados = 'setas'
            controle_selecionado = True  # Marca que o controle foi selecionado
        if button_voltar.collidepoint((mx, my)) and click:
            return controles_selecionados  # Retorna o controle selecionado

        # Se o controle foi selecionado, exibe a mensagem "Controle Selecionado"
        if controle_selecionado:
            draw_text('Controle Selecionado', fonte, vermelha, tela, 200, 150)

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
    aparecimento(tela, preta, largura, altura) # fade-in.
    controles_sel = 'setas'  # Controle padrão.

     # Som
    som_click = pygame.mixer.Sound('click.mp3')

    while True:
        button_1, button_2, button_3, button_controles = desenhar_botoes_menu(tela, fonte, branca, preta, vermelha, verde)

        mx, my = pygame.mouse.get_pos()
        acao, jogador = verificar_cliques_menu(mx, my, click, button_1, button_2, button_3, button_controles, tela, fonte, branca, preta)

        if acao == 'play':
            rodar_jogo(largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo, jogador, controles_sel)
        elif acao == 'ranking':
            som_click.play()
            exibir_ranking()
        elif acao == 'controles':
            som_click.play()
            controles_sel = selecionar_controles()  # Armazena a escolha de controle

        click = False
        for event in pygame.event.get(): # caso alt+f4... sair do jogo.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        pygame.display.update()

'''função principal, responsável por rodar o game.'''
def rodar_jogo(largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo, jogador, controles_selecionados):
    relogio = pygame.time.Clock()
    fim_jogo, x, y, velocidade_x, velocidade_y, tamanho_cobra, pixels, comida_x, comida_y = inicializar_jogo(largura, altura, tamanho_quadrado)

    # parte sonora 
    som_comendo = pygame.mixer.Sound('comer.mp3')
    bateu = pygame.mixer.Sound('bateu.mp3')

    # laço infinito até a cobrinha morrer.
    while not fim_jogo:
        tela.fill(preta)
        fim_jogo, velocidade_x, velocidade_y = processar_eventos(pygame.event.get(), controles_selecionados, velocidade_x, velocidade_y, tamanho_quadrado)

        x, y = atualizar_cobra(x, y, velocidade_x, velocidade_y, tamanho_cobra, pixels)
        if verificar_colisoes(x, y, largura, altura, pixels):
            fim_jogo = finalizar_jogo(bateu)

        desenhar_jogo(tela, verde, branca, vermelha, comida_x, comida_y, tamanho_quadrado, pixels, fonte, tamanho_cobra)

        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida(pixels, largura, altura, tamanho_quadrado)
            som_comendo.set_volume(0.1)
            som_comendo.play()

        pygame.display.update()
        relogio.tick(velocidade_jogo)

    registrar_pontuacao(jogador, tamanho_cobra - 1) # registrar a pontuação no canto superior esquerdo, abaixo do nome do jogo.
    main_menu()

# Funções auxiliares
''' função responsável por inicializar o game'''
def inicializar_jogo(largura, altura, tamanho_quadrado):
    fim_jogo, x, y = False, largura / 2, altura / 2
    velocidade_x, velocidade_y = tamanho_quadrado, 0
    tamanho_cobra, pixels = 1, []
    comida_x, comida_y = gerar_comida(pixels, largura, altura, tamanho_quadrado)
    return fim_jogo, x, y, velocidade_x, velocidade_y, tamanho_cobra, pixels, comida_x, comida_y

''' função responsável por dá direção a cobrinha.'''
def processar_eventos(eventos, controles_selecionados, velocidade_x, velocidade_y, tamanho_quadrado):
    fim_jogo = False
    for evento in eventos:
        if evento.type == pygame.QUIT:
            fim_jogo = True
        elif evento.type == pygame.KEYDOWN:
            if controles_selecionados == 'setas':
                velocidade_x, velocidade_y = movimentar_setas(evento.key, velocidade_x, velocidade_y, tamanho_quadrado)
            elif controles_selecionados == 'wasd':
                velocidade_x, velocidade_y = movimentar_wasd(evento.key, velocidade_x, velocidade_y, tamanho_quadrado)
    return fim_jogo, velocidade_x, velocidade_y

'''função para a cobrinha quando bater em algumas das bordas.'''
def finalizar_jogo(bateu):
    bateu.set_volume(0.3)
    bateu.play()
    return True

'''função para desenhar, tanto a cobrinha, a pontuação ou a comida.'''
def desenhar_jogo(tela, verde, branca, vermelha, comida_x, comida_y, tamanho_quadrado, pixels, fonte, tamanho_cobra):
    desenhar_comida(tela, verde, tamanho_quadrado, comida_x, comida_y)
    desenhar_cobra(tela, branca, tamanho_quadrado, pixels)
    desenhar_pontuacao(tela, vermelha, tamanho_cobra - 1, fonte)

'''spaw para gerar as comidas da cobrinha.'''
def gerar_comida(pixels, largura, altura, tamanho_quadrado):
    while True:
        comida_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
        comida_y = round(random.randrange(0, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
        if [comida_x, comida_y] not in pixels:
            return comida_x, comida_y
'''função desenha a comida no spaw "x"'''
def desenhar_comida(tela, verde, tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])

''' desenha a cobrinha.'''
def desenhar_cobra(tela, branca, tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

''' desenha a pontuação'''
def desenhar_pontuacao(tela, vermelha, pontuacao, fonte):
    texto = fonte.render(f"Pontos: {pontuacao}", True, vermelha)
    tela.blit(texto, [1, 1])

'''função para movimentar as setas'''
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

'''função para movimentar o controle "wasd". '''
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

'''def responsável para atualizar a cobrinha no mapa, aparecendo e desaparecendo seus píxeis.'''
def atualizar_cobra(x, y, velocidade_x, velocidade_y, tamanho_cobra, pixels):
    x += velocidade_x
    y += velocidade_y
    pixels.append([x, y])
    if len(pixels) > tamanho_cobra:
        del pixels[0]
    return x, y

# verificar quando ela bater em sí mesma ou nas bordas.
def verificar_colisoes(x, y, largura, altura, pixels):
    if x < 0 or x >= largura or y < 0 or y >= altura or [x, y] in pixels[:-1]:
        return True
    return False

# Função para registrar a pontuação
def registrar_pontuacao(jogador, pontuacao):
    with open('ranking.txt', 'a') as arq: # abri um arquivo 'txt'.
        arq.write(jogador + '\n') # jogador pula linha
        arq.write(str(pontuacao) + '\n') # pontuação pula linha

def ler_e_ordenar_ranking():
    with open('ranking.txt') as arq: 
        linhas = arq.readlines()

    ranking = []
    for i in range(0, len(linhas), 2):
        nome = linhas[i].strip()
        pontuacao = int(linhas[i + 1].strip())
        ranking.append([pontuacao, nome])

    # Ordena o ranking por pontuação em ordem decrescente (do maior para o menor)
    return sorted(ranking, reverse=True)

# Função para exibir o ranking
def exibir_ranking():
    largura, altura, tela, fonte, branca, preta, verde, vermelha, tamanho_quadrado, velocidade_jogo = configurar_jogo()
    click = False

    while True:
        tela.fill(preta)
        draw_text('Ranking', fonte, branca, tela, 300, 100)
        som_click = pygame.mixer.Sound('click.mp3')

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
            som_click.play()
            main_menu()

        pygame.draw.rect(tela, branca, button_voltar)
        draw_text('Menu', fonte, preta, tela, 350, 510)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        pygame.display.update()

# Inicializa o menu
def main():
    main_menu()

if __name__ == "__main__":
    main()